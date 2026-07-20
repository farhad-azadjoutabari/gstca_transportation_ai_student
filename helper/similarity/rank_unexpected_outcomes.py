"""Rank records with unexpected outcomes."""

from ._similarity_helpers import (
    check_columns,
    get_record_ids,
    pairwise_distance,
    prepare_feature_matrix,
    require_pandas,
)


def rank_unexpected_outcomes(
    df,
    feature_columns,
    outcome_column,
    id_column=None,
    n_neighbors=5,
    scale=True,
    metric="euclidean",
):
    """Rank records whose outcomes differ from their nearest peers.

    Use this to find tracts, roads, or intersections that behave differently
    than similar records. The expected outcome is the average outcome among the
    nearest peers based on the selected feature columns.

    Parameters
    ----------
    df : pandas.DataFrame
        Data table containing input features and outcome values.
    feature_columns : list
        Columns used to find similar peers.
    outcome_column : str
        Outcome column to compare with nearby peers.
    id_column : str, optional
        Column containing record IDs. If None, the DataFrame index is used.
    n_neighbors : int, default 5
        Number of similar peers used to estimate the expected outcome.
    scale : bool, default True
        Whether to standardize input features before measuring similarity.
    metric : {"euclidean", "manhattan"}, default "euclidean"
        Distance metric.

    Returns
    -------
    pandas.DataFrame
        Table ranked by absolute difference from expected peer outcome.

    Example
    -------
    >>> from helper.similarity import rank_unexpected_outcomes
    >>> unexpected = rank_unexpected_outcomes(roads, ["lanes", "speed_limit", "volume"], "congestion_index")
    """
    pd = require_pandas("rank_unexpected_outcomes")
    check_columns(df, [outcome_column], "outcome_column")
    matrix = prepare_feature_matrix(df, feature_columns, scale=scale)
    ids = get_record_ids(df, id_column)
    distances = pairwise_distance(matrix, metric=metric)
    outcomes = pd.to_numeric(df[outcome_column], errors="coerce").reset_index(drop=True)

    rows = []
    for i, record_id in enumerate(ids):
        neighbor_order = distances[i].argsort()
        neighbor_positions = [position for position in neighbor_order if position != i][:n_neighbors]
        neighbor_values = outcomes.iloc[neighbor_positions]
        expected = neighbor_values.mean()
        actual = outcomes.iloc[i]
        rows.append(
            {
                "id": record_id,
                "actual_outcome": actual,
                "expected_peer_outcome": expected,
                "outcome_difference": actual - expected,
                "abs_outcome_difference": abs(actual - expected),
                "nearest_peer_ids": [ids[position] for position in neighbor_positions],
            }
        )

    return pd.DataFrame(rows).sort_values("abs_outcome_difference", ascending=False).reset_index(drop=True)
