"""Summarize transportation records by time."""

from ._transportation_helpers import check_columns, require_pandas


def summarize_time_patterns(
    df,
    group_column,
    time_column,
    time_unit="hour",
    weight_column=None,
    output_count_column="record_count",
):
    """Summarize trips, crashes, or traffic records by time period.

    Use this to compare peak and off-peak patterns, weekday and weekend
    patterns, or monthly variation by tract, road, intersection, or mode.

    Parameters
    ----------
    df : pandas.DataFrame
        Data table containing a time column.
    group_column : str
        Column defining groups.
    time_column : str
        Date/time column.
    time_unit : {"hour", "day_of_week", "month", "weekday_weekend"}, default "hour"
        Time period to summarize.
    weight_column : str, optional
        Weight column to sum. If None, rows are counted.
    output_count_column : str, default "record_count"
        Name of the count or weighted sum column.

    Returns
    -------
    pandas.DataFrame
        Summary by group and time period.

    Example
    -------
    >>> from helper.transportation import summarize_time_patterns
    >>> hourly = summarize_time_patterns(crashes, "tract_id", "crash_datetime", time_unit="hour")
    """
    pd = require_pandas("summarize_time_patterns")
    check_columns(df, [group_column, time_column])
    result = df.copy()
    time_values = pd.to_datetime(result[time_column], errors="coerce")

    if time_unit == "hour":
        result["_time_period"] = time_values.dt.hour
    elif time_unit == "day_of_week":
        result["_time_period"] = time_values.dt.day_name()
    elif time_unit == "month":
        result["_time_period"] = time_values.dt.month
    elif time_unit == "weekday_weekend":
        result["_time_period"] = time_values.dt.dayofweek.map(lambda value: "weekend" if value >= 5 else "weekday")
    else:
        raise ValueError("time_unit must be one of: hour, day_of_week, month, weekday_weekend.")

    if weight_column is None:
        summary = result.groupby([group_column, "_time_period"]).size().rename(output_count_column)
    else:
        check_columns(result, [weight_column], "weight_column")
        summary = result.groupby([group_column, "_time_period"])[weight_column].sum().rename(output_count_column)

    return summary.reset_index().rename(columns={"_time_period": time_unit})
