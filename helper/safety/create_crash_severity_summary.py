"""Summarize crash severity by group."""

from ._safety_helpers import check_columns, require_pandas


def create_crash_severity_summary(df, group_column, severity_column):
    """Count crash severity categories by group.

    Use this to compare whether tracts, roads, or intersections have different
    types of crashes, not just different total crash counts.

    Parameters
    ----------
    df : pandas.DataFrame
        Crash table containing group and severity columns.
    group_column : str
        Grouping column, such as tract ID, road ID, or intersection ID.
    severity_column : str
        Crash severity column.

    Returns
    -------
    pandas.DataFrame
        One row per group with severity counts and shares.

    Example
    -------
    >>> from helper.safety import create_crash_severity_summary
    >>> severity = create_crash_severity_summary(crashes, "tract_id", "severity")
    """
    pd = require_pandas("create_crash_severity_summary")
    check_columns(df, [group_column, severity_column])
    counts = df.groupby([group_column, severity_column]).size().unstack(fill_value=0)
    counts.columns = [f"crash_{value}" for value in counts.columns]
    counts["total_crashes"] = counts.sum(axis=1)
    for column in [column for column in counts.columns if column.startswith("crash_")]:
        counts[f"share_{column.replace('crash_', '')}"] = counts[column] / counts["total_crashes"].replace(0, pd.NA)
    return counts.reset_index()
