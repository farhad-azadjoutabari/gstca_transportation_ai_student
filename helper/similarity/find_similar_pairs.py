"""Find similar pairs of records."""

from ._similarity_helpers import (
    get_record_ids,
    pairwise_distance,
    prepare_feature_matrix,
    require_pandas,
    similarity_from_distance,
)


def find_similar_pairs(
    df,
    feature_columns,
    id_column=None,
    max_pairs=100,
    scale=True,
    metric="euclidean",
):
    """Find the most similar pairs of records in a table.

    Use this to identify pairs of tracts, roads, or intersections that are
    similar based on selected input features. Students can then compare their
    outcomes, such as travel patterns, congestion, or crashes.

    Parameters
    ----------
    df : pandas.DataFrame
        Data table containing records to compare.
    feature_columns : list
        Numeric columns used to define similarity.
    id_column : str, optional
        Column containing record IDs. If None, the DataFrame index is used.
    max_pairs : int, default 100
        Maximum number of similar pairs to return.
    scale : bool, default True
        Whether to standardize features before calculating distances.
    metric : {"euclidean", "manhattan"}, default "euclidean"
        Distance metric.

    Returns
    -------
    pandas.DataFrame
        Pair table with IDs, distance, and similarity score.

    Example
    -------
    >>> from helper.similarity import find_similar_pairs
    >>> pairs = find_similar_pairs(roads, ["speed_limit", "lanes", "traffic_volume"], id_column="road_id")
    """
    pd = require_pandas("find_similar_pairs")
    matrix = prepare_feature_matrix(df, feature_columns, scale=scale)
    ids = get_record_ids(df, id_column)
    distances = pairwise_distance(matrix, metric=metric)

    rows = []
    for i, left_id in enumerate(ids):
        for j in range(i + 1, len(ids)):
            distance = float(distances[i, j])
            rows.append(
                {
                    "id_1": left_id,
                    "id_2": ids[j],
                    "similarity_distance": distance,
                    "similarity_score": float(similarity_from_distance(distance)),
                }
            )

    result = pd.DataFrame(rows).sort_values("similarity_distance").reset_index(drop=True)
    if max_pairs is not None:
        result = result.head(max_pairs)
    return result
