"""Calculate crash rates for grouped safety data."""

from helper.transportation import calculate_crash_rate


def calculate_crash_rate_by_group(
    df,
    crash_column,
    exposure_column,
    output_column="crash_rate",
    multiplier=1.0,
    zero_value=None,
):
    """Calculate crash rates for already grouped data.

    Use this after students have counted crashes by tract, road, or
    intersection and joined an exposure variable such as population, AADT, VMT,
    road miles, or entering traffic volume.

    Parameters
    ----------
    df : pandas.DataFrame
        Grouped table containing crash and exposure columns.
    crash_column : str
        Crash count column.
    exposure_column : str
        Exposure column.
    output_column : str, default "crash_rate"
        Name of the crash rate column.
    multiplier : float, default 1.0
        Multiplier for readable rates.
    zero_value : float, optional
        Value to use when exposure is zero or missing.

    Returns
    -------
    pandas.DataFrame
        Copy of the input with crash rate added.

    Example
    -------
    >>> from helper.safety import calculate_crash_rate_by_group
    >>> tracts = calculate_crash_rate_by_group(tracts, "crash_count", "population", "crashes_per_1000_people", multiplier=1000)
    """
    return calculate_crash_rate(
        df,
        crash_column=crash_column,
        exposure_column=exposure_column,
        output_column=output_column,
        multiplier=multiplier,
        zero_value=zero_value,
    )
