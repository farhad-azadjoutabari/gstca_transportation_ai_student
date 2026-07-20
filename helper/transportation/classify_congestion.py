"""Classify congestion from a speed ratio."""

from ._transportation_helpers import check_columns, require_pandas


def classify_congestion(
    df,
    speed_ratio_column="speed_ratio",
    output_column="congestion_class",
    severe_threshold=0.5,
    medium_threshold=0.8,
):
    """Classify congestion as severe, medium, or low.

    Use this after `calculate_speed_ratio`. By default, speed ratios below
    0.5 are severe, ratios from 0.5 to below 0.8 are medium, and ratios 0.8 or
    higher are low congestion.

    Parameters
    ----------
    df : pandas.DataFrame
        Road or link table containing a speed ratio column.
    speed_ratio_column : str, default "speed_ratio"
        Column with observed speed divided by free-flow speed.
    output_column : str, default "congestion_class"
        Name of the new congestion class column.
    severe_threshold : float, default 0.5
        Values below this threshold are severe congestion.
    medium_threshold : float, default 0.8
        Values below this threshold but at or above severe threshold are
        medium congestion.

    Returns
    -------
    pandas.DataFrame
        Copy of the input with congestion class added.

    Example
    -------
    >>> from helper.transportation import classify_congestion
    >>> roads = classify_congestion(roads, speed_ratio_column="speed_ratio")
    """
    pd = require_pandas("classify_congestion")
    check_columns(df, [speed_ratio_column])
    result = df.copy()
    ratio = pd.to_numeric(result[speed_ratio_column], errors="coerce")
    result[output_column] = pd.NA
    result.loc[ratio < severe_threshold, output_column] = "severe"
    result.loc[(ratio >= severe_threshold) & (ratio < medium_threshold), output_column] = "medium"
    result.loc[ratio >= medium_threshold, output_column] = "low"
    return result
