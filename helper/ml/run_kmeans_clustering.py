"""Run K-Means clustering."""

from ._ml_helpers import get_X, require_sklearn, result_dataframe


def run_kmeans_clustering(
    data,
    n_clusters=4,
    cluster_column="cluster",
    random_state=42,
    **model_kwargs,
):
    """Group rows into K-Means clusters.

    Use this when students want to group similar tracts, zones, employers, or
    other records based on several numeric features. K-Means works best when
    the input features have been scaled with `prepare_ml_data`.

    Parameters
    ----------
    data : dict or pandas.DataFrame
        Prepared ML dictionary from `prepare_ml_data` or a numeric feature
        table.
    n_clusters : int, default 4
        Number of clusters to create.
    cluster_column : str, default "cluster"
        Name of the output cluster column.
    random_state : int, default 42
        Random seed for reproducible clusters.
    **model_kwargs
        Extra options passed to `sklearn.cluster.KMeans`.

    Returns
    -------
    dict
        Dictionary with fitted `model`, cluster `labels`, and a `data` table
        containing the cluster label.

    Example
    -------
    >>> from helper.ml import prepare_ml_data, run_kmeans_clustering
    >>> ml_data = prepare_ml_data(tracts, ["population", "bus_stop_count", "total_employees"])
    >>> result = run_kmeans_clustering(ml_data, n_clusters=4)
    >>> tracts["cluster"] = result["labels"]
    """
    require_sklearn("run_kmeans_clustering")
    from sklearn.cluster import KMeans

    X = get_X(data)
    model_kwargs.setdefault("n_init", 10)
    model = KMeans(n_clusters=n_clusters, random_state=random_state, **model_kwargs)
    labels = model.fit_predict(X)

    return {
        "model": model,
        "labels": labels,
        "data": result_dataframe(X, cluster_column, labels),
        "cluster_column": cluster_column,
    }
