"""Calculate a similarity or distance matrix."""

from ._similarity_helpers import (
    get_record_ids,
    pairwise_distance,
    prepare_feature_matrix,
    require_pandas,
    similarity_from_distance,
)


def calculate_similarity_matrix(
    df,
    feature_columns,
    id_column=None,
    scale=True,
    metric="euclidean",
    return_similarity=True,
):
    """Calculate pairwise similarity between records.

    Use this to compare tracts, roads, intersections, or other records based
    on selected features. For example, students can compare neighborhoods by
    income, age, employment, and population to find demographically similar
    places.

    Parameters
    ----------
    df : pandas.DataFrame
        Data table containing records to compare.
    feature_columns : list
        Numeric columns used to measure similarity.
    id_column : str, optional
        Column used as row and column labels. If None, the DataFrame index is
        used.
    scale : bool, default True
        Whether to standardize features before calculating distances.
    metric : {"euclidean", "manhattan"}, default "euclidean"
        Distance metric.
    return_similarity : bool, default True
        If True, return similarity scores from 0 to 1. If False, return
        distances, where smaller values mean more similar records.

    Returns
    -------
    pandas.DataFrame
        Square matrix of similarity scores or distances.

    Example
    -------
    >>> from helper.similarity import calculate_similarity_matrix
    >>> matrix = calculate_similarity_matrix(tracts, ["income", "population", "median_age"], id_column="GEOID")
    """
    pd = require_pandas("calculate_similarity_matrix")
    matrix = prepare_feature_matrix(df, feature_columns, scale=scale)
    ids = get_record_ids(df, id_column)
    distances = pairwise_distance(matrix, metric=metric)
    values = similarity_from_distance(distances) if return_similarity else distances
    return pd.DataFrame(values, index=ids, columns=ids)
