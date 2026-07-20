"""Read or aggregate large CSV files in manageable chunks."""

from pathlib import Path


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


def _check_columns(df, columns, parameter_name):
    """Validate that all requested columns exist in a DataFrame."""
    missing = [column for column in columns if column not in df.columns]
    if missing:
        raise ValueError(f"{parameter_name} contains columns that were not found: {missing}")


def read_large_csv_in_chunks(
    file_path,
    chunk_size=100000,
    groupby_columns=None,
    sum_columns=None,
    mean_columns=None,
    count_column=None,
    max_rows=None,
    progress=False,
    **read_csv_kwargs,
):
    """Read a large CSV in chunks, optionally returning a grouped summary.

    This helper gives students a safer way to work with very large files such
    as OD trips or turning-movement counts. When no aggregation arguments are
    supplied, the function returns the normal pandas chunk iterator. When
    `groupby_columns`, `sum_columns`, `mean_columns`, or `count_column` are
    supplied, it processes the file chunk by chunk and returns one aggregated
    DataFrame.

    Parameters
    ----------
    file_path : str or pathlib.Path
        Path to the CSV file.
    chunk_size : int, default 100000
        Number of rows to read at a time.
    groupby_columns : str, list, or None, default None
        Columns used to group the summary, such as origin tract or TMC ID.
        Leave as None to create one overall summary row.
    sum_columns : str, list, dict, or None, default None
        Numeric columns to sum. A dictionary maps input names to output names.
    mean_columns : str, list, dict, or None, default None
        Numeric columns to average. A dictionary maps input names to output
        names.
    count_column : str or None, default None
        Optional output column for row counts in each group.
    max_rows : int or None, default None
        Optional row limit. Useful for classroom demos before running the full
        file.
    progress : bool, default False
        If True, print a short progress message after each chunk.
    **read_csv_kwargs
        Extra options passed to `pandas.read_csv`, such as `usecols`, `dtype`,
        or `encoding`.

    Returns
    -------
    pandas.io.parsers.TextFileReader or pandas.DataFrame
        A chunk iterator when no aggregation is requested, otherwise an
        aggregated DataFrame.

    Example
    -------
    >>> from helper.data_read import read_large_csv_in_chunks
    >>> origin_summary = read_large_csv_in_chunks(
    ...     "data/od_trips.csv",
    ...     groupby_columns="origin_trct_2020",
    ...     sum_columns={"trip_weight": "estimated_trips"},
    ...     count_column="sample_records",
    ... )
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")
    if path.suffix.lower() != ".csv":
        raise ValueError(f"Expected a .csv file, but got: {path.name}")
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero.")
    if max_rows is not None and max_rows <= 0:
        raise ValueError("max_rows must be greater than zero when provided.")

    try:
        import pandas as pd
    except ImportError as exc:
        raise ImportError(
            "pandas is required to read CSV files. Install it with: pip install pandas"
        ) from exc

    read_kwargs = dict(read_csv_kwargs)
    read_kwargs.setdefault("low_memory", False)

    group_columns = _as_list(groupby_columns, "groupby_columns")
    sum_mapping = _normalize_mapping(sum_columns, "sum_")
    mean_mapping = _normalize_mapping(mean_columns, "mean_")
    aggregation_requested = bool(group_columns or sum_mapping or mean_mapping or count_column)
    if group_columns and not (sum_mapping or mean_mapping or count_column):
        count_column = "row_count"

    if not aggregation_requested:
        reader = pd.read_csv(path, chunksize=chunk_size, **read_kwargs)
        if max_rows is None:
            return reader

        frames = []
        rows_read = 0
        for chunk_number, chunk in enumerate(reader, start=1):
            remaining = max_rows - rows_read
            if remaining <= 0:
                break
            frames.append(chunk.head(remaining))
            rows_read += len(frames[-1])
            if progress:
                print(f"Read {rows_read:,} rows after chunk {chunk_number:,}.")
        return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

    accumulator = None
    rows_read = 0
    dummy_group_column = "__all_rows__"
    internal_mean_columns = {}

    for chunk_number, chunk in enumerate(
        pd.read_csv(path, chunksize=chunk_size, **read_kwargs),
        start=1,
    ):
        if max_rows is not None:
            remaining = max_rows - rows_read
            if remaining <= 0:
                break
            chunk = chunk.head(remaining)

        rows_read += len(chunk)
        if chunk.empty:
            continue

        needed_columns = set(group_columns) | set(sum_mapping) | set(mean_mapping)
        _check_columns(chunk, needed_columns, "aggregation columns")

        work = chunk.copy()
        active_group_columns = list(group_columns)
        if not active_group_columns:
            active_group_columns = [dummy_group_column]
            work[dummy_group_column] = "all_rows"

        grouped = work.groupby(active_group_columns, dropna=False)
        pieces = []

        if count_column is not None:
            pieces.append(grouped.size().rename(count_column))

        for source_column, output_column in sum_mapping.items():
            values = pd.to_numeric(work[source_column], errors="coerce")
            pieces.append(values.groupby([work[column] for column in active_group_columns]).sum().rename(output_column))

        for source_column, output_column in mean_mapping.items():
            values = pd.to_numeric(work[source_column], errors="coerce")
            sum_name = f"__{output_column}_sum__"
            count_name = f"__{output_column}_count__"
            internal_mean_columns[output_column] = (sum_name, count_name)
            pieces.append(values.groupby([work[column] for column in active_group_columns]).sum().rename(sum_name))
            pieces.append(values.notna().groupby([work[column] for column in active_group_columns]).sum().rename(count_name))

        partial = pd.concat(pieces, axis=1).fillna(0)
        accumulator = partial if accumulator is None else accumulator.add(partial, fill_value=0)

        if progress:
            print(f"Processed {rows_read:,} rows after chunk {chunk_number:,}.")

    if accumulator is None:
        output_columns = []
        if count_column is not None:
            output_columns.append(count_column)
        output_columns.extend(sum_mapping.values())
        output_columns.extend(mean_mapping.values())
        return pd.DataFrame(columns=group_columns + output_columns)

    result = accumulator.reset_index()

    for output_column, (sum_name, count_name) in internal_mean_columns.items():
        denominator = result[count_name].where(result[count_name] != 0)
        result[output_column] = result[sum_name] / denominator
        result = result.drop(columns=[sum_name, count_name])

    if dummy_group_column in result.columns:
        result = result.drop(columns=dummy_group_column)

    if count_column is not None:
        result[count_column] = result[count_column].fillna(0).astype(int)

    return result
