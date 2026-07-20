"""Normalize numeric columns."""

from ._feature_helpers import check_columns, require_pandas


def normalize_columns(df, columns, method="zscore", output_suffix="_normalized"):
    """Create normalized versions of numeric columns.

    Use this before similarity analysis, clustering, PCA, KNN, or SVM so that
    variables measured in different units can be compared fairly.

    Parameters
    ----------
    df : pandas.DataFrame
        Data table containing numeric columns.
    columns : list
        Numeric columns to normalize.
    method : {"zscore", "minmax"}, default "zscore"
        Normalization method. Z-score subtracts the mean and divides by
        standard deviation. Min-max rescales values from 0 to 1.
    output_suffix : str, default "_normalized"
        Suffix added to each normalized output column.

    Returns
    -------
    pandas.DataFrame
        Copy of the input with normalized columns added.

    Example
    -------
    >>> from helper.features import normalize_columns
    >>> tracts = normalize_columns(tracts, ["income", "population", "bus_stop_count"])
    """
    pd = require_pandas("normalize_columns")
    if isinstance(columns, str):
        columns = [columns]
    check_columns(df, columns)

    result = df.copy()
    for column in columns:
        values = pd.to_numeric(result[column], errors="coerce")
        output_column = f"{column}{output_suffix}"
        if method == "zscore":
            std = values.std()
            result[output_column] = 0 if std == 0 else (values - values.mean()) / std
        elif method == "minmax":
            value_range = values.max() - values.min()
            result[output_column] = 0 if value_range == 0 else (values - values.min()) / value_range
        else:
            raise ValueError("method must be 'zscore' or 'minmax'.")
    return result
