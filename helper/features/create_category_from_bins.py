"""Create categories from numeric bins."""

from ._feature_helpers import check_columns, require_pandas


def create_category_from_bins(df, column, bins, labels, output_column, include_lowest=True):
    """Create labeled categories from numeric ranges.

    Use this to make low/medium/high classes for crash rates, congestion,
    traffic volume, speed, income, density, or accessibility.

    Parameters
    ----------
    df : pandas.DataFrame
        Data table containing the numeric column.
    column : str
        Numeric column to bin.
    bins : list
        Bin edges passed to `pandas.cut`.
    labels : list
        Labels for each bin.
    output_column : str
        Name of the new category column.
    include_lowest : bool, default True
        Whether the first interval should include the lowest value.

    Returns
    -------
    pandas.DataFrame
        Copy of the input with the new category column.

    Example
    -------
    >>> from helper.features import create_category_from_bins
    >>> roads = create_category_from_bins(roads, "speed_ratio", [0, 0.5, 0.8, 1.0], ["severe", "medium", "low"], "congestion_class")
    """
    pd = require_pandas("create_category_from_bins")
    check_columns(df, [column])
    result = df.copy()
    result[output_column] = pd.cut(
        result[column],
        bins=bins,
        labels=labels,
        include_lowest=include_lowest,
    )
    return result
