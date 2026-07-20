"""Create a binary flag from a threshold."""

from ._feature_helpers import check_columns, require_pandas


def create_binary_flag(df, column, threshold, output_column, operator=">="):
    """Create a 0/1 flag using a threshold.

    Use this to create classification targets or simple indicators, such as
    high-crash tract, high-congestion road, high-employment tract, or low
    transit-access neighborhood.

    Parameters
    ----------
    df : pandas.DataFrame
        Data table containing the source column.
    column : str
        Column used for the threshold.
    threshold : float
        Threshold value.
    output_column : str
        Name of the new flag column.
    operator : {">=", ">", "<=", "<", "==", "!="}, default ">="
        Comparison operator.

    Returns
    -------
    pandas.DataFrame
        Copy of the input with a new 0/1 flag column.

    Example
    -------
    >>> from helper.features import create_binary_flag
    >>> tracts = create_binary_flag(tracts, "crash_count", 20, "high_crash_tract")
    """
    require_pandas("create_binary_flag")
    check_columns(df, [column])
    result = df.copy()
    comparisons = {
        ">=": result[column] >= threshold,
        ">": result[column] > threshold,
        "<=": result[column] <= threshold,
        "<": result[column] < threshold,
        "==": result[column] == threshold,
        "!=": result[column] != threshold,
    }
    if operator not in comparisons:
        raise ValueError("operator must be one of: >=, >, <=, <, ==, !=.")
    result[output_column] = comparisons[operator].astype(int)
    return result
