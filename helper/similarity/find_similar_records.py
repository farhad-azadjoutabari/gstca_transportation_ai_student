"""Find records most similar to one selected record."""

from ._similarity_helpers import (
    get_record_ids,
    pairwise_distance,
    prepare_feature_matrix,
    require_pandas,
    similarity_from_distance,
)


def find_similar_records(
    df,
    id_column,
    feature_columns,
    target_id,
    n=10,
    scale=True,
    metric="euclidean",
):
    """Find records most similar to one target record.

    Use this when students choose one tract, road, or intersection and want to
    find its closest peers based on selected characteristics.

    Parameters
    ----------
    df : pandas.DataFrame
        Data table containing records to compare.
    id_column : str
        Column containing record IDs.
    feature_columns : list
        Numeric columns used to define similarity.
    target_id
        ID value of the record students want to compare against.
    n : int, default 10
        Number of similar records to return.
    scale : bool, default True
        Whether to standardize features before calculating distances.
    metric : {"euclidean", "manhattan"}, default "euclidean"
        Distance metric.

    Returns
    -------
    pandas.DataFrame
        Similar records with distance and similarity score.

    Example
    -------
    >>> from helper.similarity import find_similar_records
    >>> similar = find_similar_records(tracts, "GEOID", ["income", "population"], target_id="48113000100")
    """
    pd = require_pandas("find_similar_records")
    matrix = prepare_feature_matrix(df, feature_columns, scale=scale)
    ids = get_record_ids(df, id_column)
    if target_id not in ids:
        raise ValueError(f"target_id was not found in {id_column}: {target_id}")

    target_position = ids.index(target_id)
    distances = pairwise_distance(matrix, metric=metric)[target_position]

    result = df.copy()
    result["similarity_distance"] = distances
    result["similarity_score"] = similarity_from_distance(distances)
    result = result[result[id_column] != target_id]
    return result.sort_values("similarity_distance").head(n).reset_index(drop=True)
