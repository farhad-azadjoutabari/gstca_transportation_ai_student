"""Calculate speed ratio indicators."""

from ._transportation_helpers import check_columns, require_pandas


def calculate_speed_ratio(
    df,
    speed_column,
    free_flow_column,
    output_column="speed_ratio",
    zero_value=None,
):
    """Calculate observed speed divided by free-flow speed.

    Use this as a simple congestion indicator. Lower values usually mean more
    congestion because observed speed is much lower than free-flow speed.

    Parameters
    ----------
    df : pandas.DataFrame
        Road or link table containing speed columns.
    speed_column : str
        Observed speed column.
    free_flow_column : str
        Free-flow speed column.
    output_column : str, default "speed_ratio"
        Name of the new ratio column.
    zero_value : float, optional
        Value to use when free-flow speed is zero or missing.

    Returns
    -------
    pandas.DataFrame
        Copy of the input with speed ratio added.

    Example
    -------
    >>> from helper.transportation import calculate_speed_ratio
    >>> roads = calculate_speed_ratio(roads, "avg_speed", "free_flow_speed")
    """
    pd = require_pandas("calculate_speed_ratio")
    check_columns(df, [speed_column, free_flow_column])
    result = df.copy()
    speed = pd.to_numeric(result[speed_column], errors="coerce")
    free_flow = pd.to_numeric(result[free_flow_column], errors="coerce").replace(0, float("nan"))
    result[output_column] = speed / free_flow
    if zero_value is not None:
        result[output_column] = result[output_column].fillna(zero_value)
    return result
