"""Summarize OD trips by destination."""

from .calculate_mode_share import calculate_mode_share
from ._transportation_helpers import check_columns, require_pandas


def summarize_od_by_destination(
    od_df,
    destination_column,
    mode_column=None,
    weight_column=None,
):
    """Summarize trip records by destination geography.

    Use this when students want to understand where trips go, which tracts are
    major destinations, or whether similar origins have different destination
    patterns.

    Parameters
    ----------
    od_df : pandas.DataFrame
        OD or trip table.
    destination_column : str
        Destination geography column, such as destination tract.
    mode_column : str, optional
        Travel mode column.
    weight_column : str, optional
        Trip weight column. If None, rows are counted.

    Returns
    -------
    pandas.DataFrame
        Destination-level trip summary.

    Example
    -------
    >>> from helper.transportation import summarize_od_by_destination
    >>> destination_summary = summarize_od_by_destination(trips, "destination_trct_2020", mode_column="mode")
    """
    require_pandas("summarize_od_by_destination")
    check_columns(od_df, [destination_column])
    if mode_column is not None:
        return calculate_mode_share(od_df, destination_column, mode_column, weight_column=weight_column)

    if weight_column is None:
        return od_df.groupby(destination_column).size().rename("total_trips").reset_index()
    check_columns(od_df, [weight_column], "weight_column")
    return od_df.groupby(destination_column)[weight_column].sum().rename("total_trips").reset_index()
