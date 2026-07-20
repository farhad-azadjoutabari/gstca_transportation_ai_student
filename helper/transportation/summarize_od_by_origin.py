"""Summarize OD trips by origin."""

from .calculate_mode_share import calculate_mode_share
from ._transportation_helpers import check_columns, require_pandas


def summarize_od_by_origin(
    od_df,
    origin_column,
    mode_column=None,
    weight_column=None,
):
    """Summarize trip records by origin geography.

    Use this for Challenge 1 when students want to describe travel patterns
    for each home or origin tract. If `mode_column` is provided, the output
    includes mode counts and shares.

    Parameters
    ----------
    od_df : pandas.DataFrame
        OD or trip table.
    origin_column : str
        Origin geography column, such as origin tract.
    mode_column : str, optional
        Travel mode column.
    weight_column : str, optional
        Trip weight column. If None, rows are counted.

    Returns
    -------
    pandas.DataFrame
        Origin-level trip summary.

    Example
    -------
    >>> from helper.transportation import summarize_od_by_origin
    >>> origin_summary = summarize_od_by_origin(trips, "origin_trct_2020", mode_column="mode")
    """
    pd = require_pandas("summarize_od_by_origin")
    check_columns(od_df, [origin_column])
    if mode_column is not None:
        return calculate_mode_share(od_df, origin_column, mode_column, weight_column=weight_column)

    if weight_column is None:
        return od_df.groupby(origin_column).size().rename("total_trips").reset_index()
    check_columns(od_df, [weight_column], "weight_column")
    return od_df.groupby(origin_column)[weight_column].sum().rename("total_trips").reset_index()
