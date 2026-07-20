"""Calculate travel mode shares."""

from ._transportation_helpers import check_columns, require_pandas, weighted_count_table


def calculate_mode_share(
    df,
    group_column,
    mode_column,
    weight_column=None,
    count_prefix="trips",
    share_prefix="share",
):
    """Calculate travel mode counts and shares by group.

    Use this with OD or trip tables to compare how travel behavior differs by
    tract, home location, destination, income group, or another grouping
    column.

    Parameters
    ----------
    df : pandas.DataFrame
        Trip or OD table.
    group_column : str
        Column defining groups, such as origin tract or destination tract.
    mode_column : str
        Column containing travel mode.
    weight_column : str, optional
        Trip weight column. If None, rows are counted.
    count_prefix : str, default "trips"
        Prefix for mode count columns.
    share_prefix : str, default "share"
        Prefix for mode share columns.

    Returns
    -------
    pandas.DataFrame
        One row per group with total trips, mode counts, and mode shares.

    Example
    -------
    >>> from helper.transportation import calculate_mode_share
    >>> mode_share = calculate_mode_share(trips, "origin_trct_2020", "mode")
    """
    pd = require_pandas("calculate_mode_share")
    check_columns(df, [group_column, mode_column])
    counts = weighted_count_table(df, [group_column, mode_column], weight_column=weight_column)
    pivot = counts.pivot_table(index=group_column, columns=mode_column, values="trip_count", fill_value=0)
    pivot.columns = [f"{count_prefix}_{value}" for value in pivot.columns]
    pivot["total_trips"] = pivot.sum(axis=1)

    for column in [column for column in pivot.columns if column.startswith(f"{count_prefix}_")]:
        mode_name = column.replace(f"{count_prefix}_", "")
        pivot[f"{share_prefix}_{mode_name}"] = pivot[column] / pivot["total_trips"].replace(0, pd.NA)

    return pivot.reset_index()
