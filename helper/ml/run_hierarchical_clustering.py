"""Run hierarchical clustering."""

from ._ml_helpers import get_X, require_sklearn, result_dataframe


def run_hierarchical_clustering(
    data,
    n_clusters=4,
    linkage="ward",
    cluster_column="cluster",
    **model_kwargs,
):
    """Group rows with agglomerative hierarchical clustering.

    Use this for smaller datasets when students want an interpretable grouping
    approach. The algorithm starts with each row as its own cluster and merges
    similar rows until the requested number of clusters remains.

    Parameters
    ----------
    data : dict or pandas.DataFrame
        Prepared ML dictionary from `prepare_ml_data` or a numeric feature
        table.
    n_clusters : int, default 4
        Number of clusters to create.
    linkage : str, default "ward"
        Linkage method, such as "ward", "complete", "average", or "single".
    cluster_column : str, default "cluster"
        Name of the output cluster column.
    **model_kwargs
        Extra options passed to `sklearn.cluster.AgglomerativeClustering`.

    Returns
    -------
    dict
        Dictionary with fitted `model`, cluster `labels`, and a `data` table
        containing the cluster label.

    Example
    -------
    >>> from helper.ml import run_hierarchical_clustering
    >>> result = run_hierarchical_clustering(ml_data, n_clusters=5)
    """
    require_sklearn("run_hierarchical_clustering")
    from sklearn.cluster import AgglomerativeClustering

    X = get_X(data)
    model = AgglomerativeClustering(
        n_clusters=n_clusters,
        linkage=linkage,
        **model_kwargs,
    )
    labels = model.fit_predict(X)

    return {
        "model": model,
        "labels": labels,
        "data": result_dataframe(X, cluster_column, labels),
        "cluster_column": cluster_column,
    }
