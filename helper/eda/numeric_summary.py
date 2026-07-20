"""Summarize numeric columns."""

from ._eda_helpers import numeric_columns, require_pandas


def numeric_summary(df, columns=None):
    """Return summary statistics for numeric columns.

    Use this to inspect variables such as population, income, crash counts,
    traffic volume, speed, land area, or employment before modeling.

    Parameters
    ----------
    df : pandas.DataFrame
        Data table to summarize.
    columns : list, optional
        Numeric columns to summarize. If None, all numeric columns are used.

    Returns
    -------
    pandas.DataFrame
        Summary table with count, missing values, mean, standard deviation,
        min, quartiles, median, and max.

    Example
    -------
    >>> from helper.eda import numeric_summary
    >>> summary = numeric_summary(tracts, ["population", "total_employees"])
    """
    pd = require_pandas("numeric_summary")
    selected = numeric_columns(df, columns)
    if not selected:
        return pd.DataFrame()

    summary = df[selected].describe().transpose().reset_index().rename(columns={"index": "column"})
    missing = df[selected].isna().sum().rename("missing_count")
    summary = summary.merge(missing.reset_index().rename(columns={"index": "column"}), on="column")
    return summary
