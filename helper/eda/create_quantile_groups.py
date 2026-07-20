"""Create quantile-based groups."""

from ._eda_helpers import require_pandas


def create_quantile_groups(df, column, output_column=None, q=4, labels=None):
    """Create equal-sized groups from a numeric column.

    Use this when students need simple low/medium/high or quartile groups for
    exploration, mapping, or classification targets. For example, they can
    turn crash counts into low, medium, and high crash groups.

    Parameters
    ----------
    df : pandas.DataFrame
        Data table containing the numeric column.
    column : str
        Numeric column used to create groups.
    output_column : str, optional
        Name of the new group column. If None, uses `{column}_quantile_group`.
    q : int, default 4
        Number of quantile groups.
    labels : list, optional
        Labels for the groups. Length must match `q`.

    Returns
    -------
    pandas.DataFrame
        Copy of the input with a new quantile group column.

    Example
    -------
    >>> from helper.eda import create_quantile_groups
    >>> tracts = create_quantile_groups(tracts, "crash_count", q=3, labels=["low", "medium", "high"])
    """
    pd = require_pandas("create_quantile_groups")
    if column not in df.columns:
        raise ValueError(f"column was not found: {column}")
    if output_column is None:
        output_column = f"{column}_quantile_group"

    result = df.copy()
    result[output_column] = pd.qcut(
        result[column],
        q=q,
        labels=labels,
        duplicates="drop",
    )
    return result
