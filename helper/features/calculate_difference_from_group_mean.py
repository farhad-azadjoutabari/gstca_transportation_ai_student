"""Compare values with their group average."""

from ._feature_helpers import check_columns, require_pandas


def calculate_difference_from_group_mean(
    df,
    group_column,
    value_column,
    output_column=None,
    group_mean_column=None,
):
    """Calculate how far each row is from its group average.

    Use this to find roads, tracts, or intersections that behave differently
    from similar peers. For example, students can compare each road's
    congestion to the average congestion of roads with the same class and
    speed limit.

    Parameters
    ----------
    df : pandas.DataFrame
        Data table containing group and value columns.
    group_column : str
        Column defining similar groups.
    value_column : str
        Numeric column to compare with the group mean.
    output_column : str, optional
        Name of the difference column. If None, uses
        `{value_column}_minus_group_mean`.
    group_mean_column : str, optional
        Name of the group mean column. If None, uses
        `{value_column}_group_mean`.

    Returns
    -------
    pandas.DataFrame
        Copy of the input with group mean and difference columns.

    Example
    -------
    >>> from helper.features import calculate_difference_from_group_mean
    >>> roads = calculate_difference_from_group_mean(roads, "road_class", "congestion_index")
    """
    require_pandas("calculate_difference_from_group_mean")
    check_columns(df, [group_column, value_column])
    if output_column is None:
        output_column = f"{value_column}_minus_group_mean"
    if group_mean_column is None:
        group_mean_column = f"{value_column}_group_mean"

    result = df.copy()
    result[group_mean_column] = result.groupby(group_column)[value_column].transform("mean")
    result[output_column] = result[value_column] - result[group_mean_column]
    return result
