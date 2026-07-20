"""Summarize columns in a data table."""

from ._eda_helpers import require_pandas


def summarize_columns(df):
    """Return a quick summary of every column in a DataFrame.

    Use this after reading or joining data to understand what columns are
    available, their data types, how many values are missing, and how many
    unique values each column contains.

    Parameters
    ----------
    df : pandas.DataFrame
        Data table to summarize.

    Returns
    -------
    pandas.DataFrame
        One row per column with data type, missing values, unique values, and
        an example non-missing value.

    Example
    -------
    >>> from helper.eda import summarize_columns
    >>> column_summary = summarize_columns(tracts)
    >>> column_summary.head()
    """
    pd = require_pandas("summarize_columns")
    row_count = len(df)
    rows = []
    for column in df.columns:
        non_missing = df[column].dropna()
        rows.append(
            {
                "column": column,
                "dtype": str(df[column].dtype),
                "missing_count": int(df[column].isna().sum()),
                "missing_percent": float(df[column].isna().mean() * 100) if row_count else 0.0,
                "unique_count": int(df[column].nunique(dropna=True)),
                "example_value": non_missing.iloc[0] if not non_missing.empty else pd.NA,
            }
        )
    return pd.DataFrame(rows)
