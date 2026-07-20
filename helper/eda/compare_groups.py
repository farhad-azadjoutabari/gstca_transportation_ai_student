"""Compare numeric values across groups."""

from ._eda_helpers import normalize_columns, require_pandas


def compare_groups(df, group_column, value_columns, agg_funcs=("count", "mean", "median", "min", "max")):
    """Compare numeric variables by group.

    Use this after creating groups such as clusters, high/medium/low crash
    categories, congestion levels, road classes, or demographic groups.

    Parameters
    ----------
    df : pandas.DataFrame
        Data table containing groups and values.
    group_column : str
        Column defining groups.
    value_columns : str or list
        Numeric columns to summarize within each group.
    agg_funcs : tuple, default ("count", "mean", "median", "min", "max")
        Summary statistics to calculate.

    Returns
    -------
    pandas.DataFrame
        Group comparison table.

    Example
    -------
    >>> from helper.eda import compare_groups
    >>> comparison = compare_groups(tracts, "cluster", ["crash_count", "total_employees"])
    """
    require_pandas("compare_groups")
    if group_column not in df.columns:
        raise ValueError(f"group_column was not found: {group_column}")
    selected = normalize_columns(value_columns, df, "value_columns")
    return df.groupby(group_column)[selected].agg(list(agg_funcs)).reset_index()
