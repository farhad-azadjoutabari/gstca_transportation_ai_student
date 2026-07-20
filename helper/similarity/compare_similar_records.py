"""Compare similar records with different outcomes."""

from ._similarity_helpers import check_columns, require_pandas
from .find_similar_pairs import find_similar_pairs


def compare_similar_records(
    df,
    feature_columns,
    outcome_column,
    id_column=None,
    max_pairs=100,
    scale=True,
    metric="euclidean",
):
    """Find similar records that have different outcomes.

    This function directly supports questions like "Why do similar
    neighborhoods have different travel patterns?" or "Why do similar roads
    have different congestion?" It first finds similar pairs using input
    features, then compares the outcome difference between each pair.

    Parameters
    ----------
    df : pandas.DataFrame
        Data table containing input features and an outcome column.
    feature_columns : list
        Columns used to define similarity.
    outcome_column : str
        Outcome column to compare, such as crash count, congestion score, or
        transit mode share.
    id_column : str, optional
        Column containing record IDs. If None, the DataFrame index is used.
    max_pairs : int, default 100
        Number of pairs to return after ranking.
    scale : bool, default True
        Whether to standardize input features before measuring similarity.
    metric : {"euclidean", "manhattan"}, default "euclidean"
        Distance metric.

    Returns
    -------
    pandas.DataFrame
        Pair table with similarity distance, outcome values, outcome
        difference, and unexpectedness score.

    Example
    -------
    >>> from helper.similarity import compare_similar_records
    >>> pairs = compare_similar_records(
    ...     tracts,
    ...     ["income", "population", "education_share"],
    ...     outcome_column="transit_mode_share",
    ...     id_column="GEOID",
    ... )
    """
    pd = require_pandas("compare_similar_records")
    check_columns(df, [outcome_column], "outcome_column")
    pairs = find_similar_pairs(
        df,
        feature_columns,
        id_column=id_column,
        max_pairs=None,
        scale=scale,
        metric=metric,
    )

    id_values = list(df[id_column]) if id_column is not None else list(df.index)
    outcome_lookup = dict(zip(id_values, pd.to_numeric(df[outcome_column], errors="coerce")))
    pairs[f"{outcome_column}_1"] = pairs["id_1"].map(outcome_lookup)
    pairs[f"{outcome_column}_2"] = pairs["id_2"].map(outcome_lookup)
    pairs["outcome_difference"] = (
        pairs[f"{outcome_column}_1"] - pairs[f"{outcome_column}_2"]
    ).abs()
    pairs["unexpected_score"] = pairs["outcome_difference"] * pairs["similarity_score"]

    return (
        pairs.sort_values(["unexpected_score", "similarity_score"], ascending=[False, False])
        .head(max_pairs)
        .reset_index(drop=True)
    )
