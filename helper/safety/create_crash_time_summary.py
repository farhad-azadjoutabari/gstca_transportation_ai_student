"""Summarize crashes by time."""

from helper.transportation import summarize_time_patterns


def create_crash_time_summary(
    crash_df,
    group_column,
    time_column,
    time_unit="hour",
):
    """Summarize crash counts by time period and group.

    Use this to compare when crashes occur across tracts, roads, or
    intersections. Common choices include hour, day of week, month, and
    weekday/weekend.

    Parameters
    ----------
    crash_df : pandas.DataFrame
        Crash table containing group and time columns.
    group_column : str
        Grouping column, such as tract ID, road ID, or intersection ID.
    time_column : str
        Crash date or datetime column.
    time_unit : {"hour", "day_of_week", "month", "weekday_weekend"}, default "hour"
        Time period to summarize.

    Returns
    -------
    pandas.DataFrame
        Crash count summary by group and time period.

    Example
    -------
    >>> from helper.safety import create_crash_time_summary
    >>> hourly = create_crash_time_summary(crashes, "intersection_id", "crash_datetime")
    """
    return summarize_time_patterns(
        crash_df,
        group_column=group_column,
        time_column=time_column,
        time_unit=time_unit,
        output_count_column="crash_count",
    )
