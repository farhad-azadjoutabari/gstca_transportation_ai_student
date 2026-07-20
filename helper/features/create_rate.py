"""Create a rate variable."""

from ._feature_helpers import check_columns, require_pandas, safe_divide


def create_rate(df, numerator, denominator, output_column, multiplier=1.0, zero_value=None):
    """Create a rate from a numerator and denominator.

    Use this to normalize outcomes by exposure, such as crashes per 1,000
    residents, crashes per million vehicle miles, employers per tract, or
    transit stops per square mile.

    Parameters
    ----------
    df : pandas.DataFrame
        Data table containing the numerator and denominator.
    numerator : str
        Column on top of the rate.
    denominator : str
        Column on bottom of the rate.
    output_column : str
        Name of the new rate column.
    multiplier : float, default 1.0
        Multiplier for readable rates, such as 1000 or 1000000.
    zero_value : float, optional
        Value to use when the denominator is zero or missing. If None, the
        result is missing.

    Returns
    -------
    pandas.DataFrame
        Copy of the input with the new rate column.

    Example
    -------
    >>> from helper.features import create_rate
    >>> tracts = create_rate(tracts, "crash_count", "population", "crashes_per_1000_people", multiplier=1000)
    """
    pd = require_pandas("create_rate")
    check_columns(df, [numerator, denominator])
    result = df.copy()
    top = pd.to_numeric(result[numerator], errors="coerce")
    bottom = pd.to_numeric(result[denominator], errors="coerce")
    result[output_column] = safe_divide(top, bottom, zero_value=zero_value) * multiplier
    return result
