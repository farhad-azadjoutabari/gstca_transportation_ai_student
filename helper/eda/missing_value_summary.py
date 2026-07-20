"""Summarize missing values."""

from ._eda_helpers import require_pandas


def missing_value_summary(df, only_missing=True):
    """Summarize missing values by column.

    Use this before analysis or machine learning to decide which variables may
    need cleaning, imputation, or removal.

    Parameters
    ----------
    df : pandas.DataFrame
        Data table to check.
    only_missing : bool, default True
        If True, return only columns with at least one missing value.

    Returns
    -------
    pandas.DataFrame
        Columns with missing value counts and percentages.

    Example
    -------
    >>> from helper.eda import missing_value_summary
    >>> missing = missing_value_summary(tracts)
    """
    pd = require_pandas("missing_value_summary")
    result = pd.DataFrame(
        {
            "column": df.columns,
            "missing_count": df.isna().sum().astype(int).values,
            "missing_percent": (df.isna().mean() * 100).values,
        }
    ).sort_values("missing_count", ascending=False)

    if only_missing:
        result = result[result["missing_count"] > 0]
    return result.reset_index(drop=True)
