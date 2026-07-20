"""Create a share or percentage variable."""

from .create_rate import create_rate


def create_share(df, part_column, total_column, output_column, percent=True, zero_value=None):
    """Create a share from part and total columns.

    Use this to calculate mode share, employment share, land-use share,
    percentage of crashes that are severe, or share of households without
    vehicles.

    Parameters
    ----------
    df : pandas.DataFrame
        Data table containing part and total columns.
    part_column : str
        Numerator column.
    total_column : str
        Denominator column.
    output_column : str
        Name of the new share column.
    percent : bool, default True
        If True, multiply by 100. If False, keep the share from 0 to 1.
    zero_value : float, optional
        Value to use when the denominator is zero or missing.

    Returns
    -------
    pandas.DataFrame
        Copy of the input with the new share column.

    Example
    -------
    >>> from helper.features import create_share
    >>> tracts = create_share(tracts, "transit_trips", "all_trips", "transit_mode_share")
    """
    return create_rate(
        df,
        part_column,
        total_column,
        output_column,
        multiplier=100.0 if percent else 1.0,
        zero_value=zero_value,
    )
