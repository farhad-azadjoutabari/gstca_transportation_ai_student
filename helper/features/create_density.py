"""Create a density variable."""

from .create_rate import create_rate


def create_density(df, value_column, area_column, output_column, area_multiplier=1.0, zero_value=None):
    """Create a density value using an area column.

    Use this for measures such as population density, employer density, crash
    density, bus stop density, or apartment density. The area column should
    already be in the unit students want to use, such as acres or square miles.

    Parameters
    ----------
    df : pandas.DataFrame
        Data table containing the value and area columns.
    value_column : str
        Count or amount to divide by area.
    area_column : str
        Area column.
    output_column : str
        Name of the new density column.
    area_multiplier : float, default 1.0
        Optional multiplier for readable density units.
    zero_value : float, optional
        Value to use when the area is zero or missing.

    Returns
    -------
    pandas.DataFrame
        Copy of the input with the new density column.

    Example
    -------
    >>> from helper.features import create_density
    >>> tracts = create_density(tracts, "total_employees", "area_sq_miles", "employees_per_sq_mile")
    """
    return create_rate(
        df,
        value_column,
        area_column,
        output_column,
        multiplier=area_multiplier,
        zero_value=zero_value,
    )
