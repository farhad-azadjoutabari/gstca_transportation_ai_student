"""Compare K-Means cluster counts."""

from ._ml_helpers import get_X, require_pandas, require_sklearn


def find_best_k_for_kmeans(data, k_values=range(2, 11), random_state=42, **model_kwargs):
    """Test several K-Means cluster counts.

    Use this before final K-Means clustering to help students choose a
    reasonable number of clusters. Lower inertia is better, while higher
    silhouette score is usually better.

    Parameters
    ----------
    data : dict or pandas.DataFrame
        Prepared ML dictionary from `prepare_ml_data` or a numeric feature
        table.
    k_values : iterable, default range(2, 11)
        Cluster counts to test.
    random_state : int, default 42
        Random seed for reproducible results.
    **model_kwargs
        Extra options passed to `sklearn.cluster.KMeans`.

    Returns
    -------
    pandas.DataFrame
        Table with `n_clusters`, `inertia`, and `silhouette_score`.

    Example
    -------
    >>> from helper.ml import find_best_k_for_kmeans
    >>> scores = find_best_k_for_kmeans(ml_data, k_values=range(2, 8))
    """
    require_sklearn("find_best_k_for_kmeans")
    pd = require_pandas("find_best_k_for_kmeans")
    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_score

    X = get_X(data)
    rows = []
    model_kwargs.setdefault("n_init", 10)

    for k in k_values:
        model = KMeans(n_clusters=k, random_state=random_state, **model_kwargs)
        labels = model.fit_predict(X)
        silhouette = None
        if len(set(labels)) > 1 and len(labels) > k:
            silhouette = silhouette_score(X, labels)
        rows.append(
            {
                "n_clusters": k,
                "inertia": model.inertia_,
                "silhouette_score": silhouette,
            }
        )

    return pd.DataFrame(rows)
