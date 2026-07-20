"""Create a correlation table."""

from ._eda_helpers import numeric_columns, require_pandas


def correlation_table(df, columns=None, method="pearson", min_abs_correlation=0.0):
    """Return pairwise correlations as a sortable table.

    Use this during exploration to identify relationships between variables,
    such as whether crash counts are related to traffic volume, speed limits,
    employment, or transit access.

    Parameters
    ----------
    df : pandas.DataFrame
        Data table to analyze.
    columns : list, optional
        Numeric columns to include. If None, all numeric columns are used.
    method : {"pearson", "spearman", "kendall"}, default "pearson"
        Correlation method.
    min_abs_correlation : float, default 0.0
        Keep only pairs with absolute correlation at least this value.

    Returns
    -------
    pandas.DataFrame
        Table with column pairs, correlation, and absolute correlation.

    Example
    -------
    >>> from helper.eda import correlation_table
    >>> correlations = correlation_table(tracts, ["crash_count", "population", "bus_stop_count"])
    """
    pd = require_pandas("correlation_table")
    selected = numeric_columns(df, columns)
    corr = df[selected].corr(method=method)
    rows = []
    for i, left in enumerate(selected):
        for right in selected[i + 1 :]:
            value = corr.loc[left, right]
            if pd.notna(value) and abs(value) >= min_abs_correlation:
                rows.append(
                    {
                        "column_1": left,
                        "column_2": right,
                        "correlation": float(value),
                        "abs_correlation": float(abs(value)),
                    }
                )
    return pd.DataFrame(rows).sort_values("abs_correlation", ascending=False).reset_index(drop=True)
