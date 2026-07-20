"""Run DBSCAN clustering."""

from ._ml_helpers import get_X, require_sklearn, result_dataframe


def run_dbscan_clustering(
    data,
    eps=0.5,
    min_samples=5,
    cluster_column="cluster",
    **model_kwargs,
):
    """Find dense clusters and outliers with DBSCAN.

    Use this when students want clusters based on density rather than a fixed
    number of groups. DBSCAN can also identify outliers, which receive the
    cluster label `-1`. It works best when the input features have been scaled.

    Parameters
    ----------
    data : dict or pandas.DataFrame
        Prepared ML dictionary from `prepare_ml_data` or a numeric feature
        table.
    eps : float, default 0.5
        Neighborhood distance used by DBSCAN.
    min_samples : int, default 5
        Minimum nearby records needed to form a dense cluster.
    cluster_column : str, default "cluster"
        Name of the output cluster column.
    **model_kwargs
        Extra options passed to `sklearn.cluster.DBSCAN`.

    Returns
    -------
    dict
        Dictionary with fitted `model`, cluster `labels`, and a `data` table
        containing the cluster label.

    Example
    -------
    >>> from helper.ml import run_dbscan_clustering
    >>> result = run_dbscan_clustering(ml_data, eps=0.8, min_samples=6)
    """
    require_sklearn("run_dbscan_clustering")
    from sklearn.cluster import DBSCAN

    X = get_X(data)
    model = DBSCAN(eps=eps, min_samples=min_samples, **model_kwargs)
    labels = model.fit_predict(X)

    return {
        "model": model,
        "labels": labels,
        "data": result_dataframe(X, cluster_column, labels),
        "cluster_column": cluster_column,
    }
