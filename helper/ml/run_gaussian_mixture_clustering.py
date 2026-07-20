"""Run Gaussian Mixture clustering."""

from ._ml_helpers import get_X, require_sklearn, result_dataframe


def run_gaussian_mixture_clustering(
    data,
    n_components=4,
    cluster_column="cluster",
    random_state=42,
    **model_kwargs,
):
    """Group rows with a Gaussian Mixture Model.

    Use this when students want probabilistic clusters. Unlike K-Means, a
    Gaussian Mixture Model can also estimate the probability that each row
    belongs to each cluster.

    Parameters
    ----------
    data : dict or pandas.DataFrame
        Prepared ML dictionary from `prepare_ml_data` or a numeric feature
        table.
    n_components : int, default 4
        Number of mixture components or clusters.
    cluster_column : str, default "cluster"
        Name of the output cluster column.
    random_state : int, default 42
        Random seed for reproducible clusters.
    **model_kwargs
        Extra options passed to `sklearn.mixture.GaussianMixture`.

    Returns
    -------
    dict
        Dictionary with fitted `model`, cluster `labels`, membership
        `probabilities`, and a `data` table containing the cluster label.

    Example
    -------
    >>> from helper.ml import run_gaussian_mixture_clustering
    >>> result = run_gaussian_mixture_clustering(ml_data, n_components=4)
    """
    require_sklearn("run_gaussian_mixture_clustering")
    from sklearn.mixture import GaussianMixture

    X = get_X(data)
    model = GaussianMixture(n_components=n_components, random_state=random_state, **model_kwargs)
    labels = model.fit_predict(X)
    probabilities = model.predict_proba(X)

    return {
        "model": model,
        "labels": labels,
        "probabilities": probabilities,
        "data": result_dataframe(X, cluster_column, labels),
        "cluster_column": cluster_column,
    }
