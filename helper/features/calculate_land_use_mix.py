"""Calculate a land-use mix or diversity index."""

from ._feature_helpers import check_columns, require_pandas


def calculate_land_use_mix(
    df,
    area_columns,
    output_column="land_use_mix",
    normalize=True,
    zero_value=0,
):
    """Calculate an entropy-based mix index from land-use area columns.

    Use this after summarizing land-use polygons by category. The index is 0
    when one land use dominates and approaches 1 when area is evenly balanced
    across the selected categories.

    Parameters
    ----------
    df : pandas.DataFrame
        Data table containing land-use area columns.
    area_columns : list
        Columns containing area by land-use category, such as residential,
        commercial, industrial, and institutional acres.
    output_column : str, default "land_use_mix"
        Name of the new diversity-index column.
    normalize : bool, default True
        If True, divide entropy by the maximum possible entropy so the index is
        scaled from 0 to 1.
    zero_value : float, default 0
        Value to use when all selected area columns are zero or missing.

    Returns
    -------
    pandas.DataFrame
        Copy of the input with the land-use mix column added.

    Example
    -------
    >>> from helper.features import calculate_land_use_mix
    >>> tracts = calculate_land_use_mix(
    ...     tracts,
    ...     ["acres_residential", "acres_commercial", "acres_institutional"],
    ... )
    """
    pd = require_pandas("calculate_land_use_mix")
    import numpy as np

    if isinstance(area_columns, str):
        columns = [area_columns]
    else:
        columns = list(area_columns)

    if not columns:
        raise ValueError("area_columns must contain at least one column.")

    check_columns(df, columns, "area_columns")

    result = df.copy()
    values = result[columns].apply(pd.to_numeric, errors="coerce").clip(lower=0).fillna(0)
    totals = values.sum(axis=1)
    proportions = values.div(totals.replace(0, float("nan")), axis=0)
    positive_proportions = proportions.where(proportions > 0)
    entropy = -(positive_proportions * np.log(positive_proportions)).sum(axis=1)

    if normalize:
        if len(columns) > 1:
            entropy = entropy / np.log(len(columns))
        else:
            entropy = entropy * 0

    result[output_column] = entropy.where(totals > 0, zero_value)
    if zero_value is not None:
        result[output_column] = result[output_column].fillna(zero_value)

    return result
