"""Evaluate clustering results."""

from ._ml_helpers import get_X, require_pandas, require_sklearn


def evaluate_clustering(data, labels):
    """Calculate simple clustering quality metrics.

    Use this after clustering to understand how many records are in each
    cluster and whether the clusters are separated well. Silhouette scores
    closer to 1 are usually better; values near 0 mean clusters overlap.

    Parameters
    ----------
    data : dict or pandas.DataFrame
        Prepared ML dictionary from `prepare_ml_data` or a numeric feature
        table.
    labels : array-like
        Cluster labels from a clustering model.

    Returns
    -------
    dict
        Dictionary with cluster counts and available clustering metrics.

    Example
    -------
    >>> from helper.ml import run_kmeans_clustering, evaluate_clustering
    >>> result = run_kmeans_clustering(ml_data, n_clusters=4)
    >>> metrics = evaluate_clustering(ml_data, result["labels"])
    """
    require_sklearn("evaluate_clustering")
    pd = require_pandas("evaluate_clustering")
    from sklearn.metrics import calinski_harabasz_score, davies_bouldin_score, silhouette_score

    X = get_X(data)
    labels_series = pd.Series(labels, name="cluster")
    unique_labels = sorted(labels_series.dropna().unique())
    valid_labels = [label for label in unique_labels if label != -1]

    metrics = {
        "n_clusters": len(valid_labels),
        "n_noise": int((labels_series == -1).sum()),
        "cluster_counts": labels_series.value_counts().sort_index().to_dict(),
        "silhouette_score": None,
        "calinski_harabasz_score": None,
        "davies_bouldin_score": None,
    }

    if len(unique_labels) > 1 and len(labels_series) > len(unique_labels):
        metrics["silhouette_score"] = silhouette_score(X, labels)
        metrics["calinski_harabasz_score"] = calinski_harabasz_score(X, labels)
        metrics["davies_bouldin_score"] = davies_bouldin_score(X, labels)

    return metrics
