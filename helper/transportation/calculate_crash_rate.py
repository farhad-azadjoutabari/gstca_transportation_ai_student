"""Calculate transportation crash rates."""

from helper.features import create_rate


def calculate_crash_rate(
    df,
    crash_column,
    exposure_column,
    output_column="crash_rate",
    multiplier=1.0,
    zero_value=None,
):
    """Calculate crashes divided by an exposure variable.

    Use this to compare safety across places or roads with different exposure
    levels. Exposure can be population, AADT, vehicle miles traveled, road
    length, intersection volume, or another measure of opportunity for crashes.

    Parameters
    ----------
    df : pandas.DataFrame
        Data table containing crash and exposure columns.
    crash_column : str
        Crash count column.
    exposure_column : str
        Exposure column, such as traffic volume or population.
    output_column : str, default "crash_rate"
        Name of the new crash rate column.
    multiplier : float, default 1.0
        Multiplier for readable rates, such as 1000 or 1000000.
    zero_value : float, optional
        Value to use when exposure is zero or missing.

    Returns
    -------
    pandas.DataFrame
        Copy of the input with crash rate added.

    Example
    -------
    >>> from helper.transportation import calculate_crash_rate
    >>> tracts = calculate_crash_rate(tracts, "crash_count", "population", "crashes_per_1000_people", multiplier=1000)
    """
    return create_rate(
        df,
        crash_column,
        exposure_column,
        output_column,
        multiplier=multiplier,
        zero_value=zero_value,
    )
