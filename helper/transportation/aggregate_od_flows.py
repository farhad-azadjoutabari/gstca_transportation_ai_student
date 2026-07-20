"""Aggregate origin-destination flow records."""

from ._transportation_helpers import check_columns, require_pandas


def _as_list(value, parameter_name):
    """Normalize a string/list parameter into a list."""
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    try:
        return list(value)
    except TypeError as exc:
        raise TypeError(f"{parameter_name} must be a string, list, tuple, or None.") from exc


def _normalize_mapping(columns, default_prefix):
    """Normalize columns into an input-column to output-column mapping."""
    if columns is None:
        return {}
    if isinstance(columns, str):
        return {columns: f"{default_prefix}{columns}"}
    if isinstance(columns, dict):
        return dict(columns)
    return {column: f"{default_prefix}{column}" for column in columns}


def _iter_chunks(od_data, pd):
    """Yield one or many OD chunks."""
    if isinstance(od_data, pd.DataFrame):
        yield od_data
        return

    for chunk in od_data:
        yield chunk


def aggregate_od_flows(
    od_data,
    origin_column,
    destination_column=None,
    mode_column=None,
    time_column=None,
    groupby_columns=None,
    weight_column=None,
    sum_columns=None,
    mean_columns=None,
    flow_column="trip_count",
    share_column="flow_share",
    top_n_destinations=None,
):
    """Aggregate OD or trip records by origin, destination, mode, and time.

    Use this for Challenge 1 when a raw OD table is too detailed for analysis.
    The function works with either a normal DataFrame or a chunk iterator from
    `read_large_csv_in_chunks`, so students can summarize large trip files
    without writing their own chunked groupby logic.

    Parameters
    ----------
    od_data : pandas.DataFrame or iterable of pandas.DataFrame
        OD/trip records or a chunk iterator.
    origin_column : str
        Origin geography column.
    destination_column : str, optional
        Destination geography column.
    mode_column : str, optional
        Travel mode column.
    time_column : str, optional
        Time-period column such as hour, day, or period.
    groupby_columns : list, optional
        Full custom grouping. If provided, it replaces the origin/destination/
        mode/time construction.
    weight_column : str, optional
        Trip weight column. If None, rows are counted.
    sum_columns : str, list, dict, or None, default None
        Additional numeric columns to sum.
    mean_columns : str, list, dict, or None, default None
        Additional numeric columns to average.
    flow_column : str, default "trip_count"
        Output column for row counts or weighted trip totals.
    share_column : str or None, default "flow_share"
        Optional output column for shares within the appropriate origin group.
        With modes, this is mode share. With destinations, this is destination
        share from each origin.
    top_n_destinations : int or None, default None
        If supplied, keep only the top N destinations per origin.

    Returns
    -------
    pandas.DataFrame
        Aggregated OD flow table.

    Example
    -------
    >>> from helper.data_read import read_large_csv_in_chunks
    >>> from helper.transportation import aggregate_od_flows
    >>> chunks = read_large_csv_in_chunks("data/od.csv", usecols=["origin", "dest", "mode"])
    >>> flows = aggregate_od_flows(chunks, "origin", "dest", mode_column="mode")
    """
    pd = require_pandas("aggregate_od_flows")
    if top_n_destinations is not None and top_n_destinations <= 0:
        raise ValueError("top_n_destinations must be greater than zero when provided.")

    if groupby_columns is None:
        group_columns = [origin_column]
        for column in [destination_column, mode_column, time_column]:
            if column is not None and column not in group_columns:
                group_columns.append(column)
    else:
        group_columns = _as_list(groupby_columns, "groupby_columns")
    if not group_columns:
        raise ValueError("At least one grouping column is required.")

    sum_mapping = _normalize_mapping(sum_columns, "sum_")
    mean_mapping = _normalize_mapping(mean_columns, "mean_")
    accumulator = None
    mean_internal_columns = {}

    for chunk in _iter_chunks(od_data, pd):
        if chunk.empty:
            continue

        needed_columns = set(group_columns) | set(sum_mapping) | set(mean_mapping)
        if weight_column is not None:
            needed_columns.add(weight_column)
        check_columns(chunk, needed_columns, "OD aggregation columns")

        grouped = chunk.groupby(group_columns, dropna=False)
        pieces = []
        if weight_column is None:
            pieces.append(grouped.size().rename(flow_column))
        else:
            weights = pd.to_numeric(chunk[weight_column], errors="coerce").fillna(0)
            pieces.append(weights.groupby([chunk[column] for column in group_columns]).sum().rename(flow_column))

        for source_column, output_column in sum_mapping.items():
            values = pd.to_numeric(chunk[source_column], errors="coerce").fillna(0)
            pieces.append(values.groupby([chunk[column] for column in group_columns]).sum().rename(output_column))

        for source_column, output_column in mean_mapping.items():
            values = pd.to_numeric(chunk[source_column], errors="coerce")
            sum_name = f"__{output_column}_sum__"
            count_name = f"__{output_column}_count__"
            mean_internal_columns[output_column] = (sum_name, count_name)
            pieces.append(values.groupby([chunk[column] for column in group_columns]).sum().rename(sum_name))
            pieces.append(values.notna().groupby([chunk[column] for column in group_columns]).sum().rename(count_name))

        partial = pd.concat(pieces, axis=1).fillna(0)
        accumulator = partial if accumulator is None else accumulator.add(partial, fill_value=0)

    if accumulator is None:
        return pd.DataFrame(columns=group_columns + [flow_column])

    result = accumulator.reset_index()
    for output_column, (sum_name, count_name) in mean_internal_columns.items():
        denominator = result[count_name].where(result[count_name] != 0)
        result[output_column] = result[sum_name] / denominator
        result = result.drop(columns=[sum_name, count_name])

    if share_column is not None:
        if mode_column is not None and mode_column in group_columns:
            denominator_columns = [column for column in group_columns if column != mode_column]
        elif destination_column is not None and destination_column in group_columns:
            denominator_columns = [column for column in group_columns if column != destination_column]
        else:
            denominator_columns = []

        if denominator_columns:
            totals = result.groupby(denominator_columns, dropna=False)[flow_column].transform("sum")
            result[share_column] = result[flow_column] / totals.where(totals != 0)
        else:
            totals = result[flow_column].sum()
            result[share_column] = result[flow_column] / totals if totals else pd.NA

    if top_n_destinations is not None:
        if destination_column is None or destination_column not in group_columns:
            raise ValueError("top_n_destinations requires destination_column in the grouping.")
        rank_columns = [origin_column]
        if time_column is not None and time_column in group_columns:
            rank_columns.append(time_column)
        result["_destination_rank"] = result.groupby(rank_columns, dropna=False)[flow_column].rank(
            method="first",
            ascending=False,
        )
        result = result.loc[result["_destination_rank"] <= top_n_destinations].drop(
            columns="_destination_rank"
        )

    return result.sort_values(group_columns).reset_index(drop=True)
