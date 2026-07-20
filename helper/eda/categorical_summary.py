"""Summarize categorical columns."""

from ._eda_helpers import normalize_columns, require_pandas


def categorical_summary(df, columns=None, top_n=10, include_missing=True):
    """Count the most common values in categorical columns.

    Use this to inspect variables such as road class, congestion severity,
    development status, land-use type, crash severity, or signal type.

    Parameters
    ----------
    df : pandas.DataFrame
        Data table to summarize.
    columns : list, optional
        Categorical columns to summarize. If None, object, category, and
        boolean columns are used.
    top_n : int, default 10
        Number of most common values to return for each column.
    include_missing : bool, default True
        Whether to include missing values in the counts.

    Returns
    -------
    pandas.DataFrame
        Long table with column name, value, count, and percent.

    Example
    -------
    >>> from helper.eda import categorical_summary
    >>> summary = categorical_summary(roads, ["road_class", "congestion_level"])
    """
    pd = require_pandas("categorical_summary")
    if columns is None:
        selected = list(df.select_dtypes(include=["object", "category", "bool"]).columns)
    else:
        selected = normalize_columns(columns, df)

    rows = []
    total = len(df)
    for column in selected:
        counts = df[column].value_counts(dropna=not include_missing).head(top_n)
        for value, count in counts.items():
            rows.append(
                {
                    "column": column,
                    "value": value,
                    "count": int(count),
                    "percent": float(count / total * 100) if total else 0.0,
                }
            )
    return pd.DataFrame(rows)
