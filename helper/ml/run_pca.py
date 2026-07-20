"""Run principal component analysis."""

from ._ml_helpers import get_X, require_pandas, require_sklearn, safe_feature_names


def run_pca(data, n_components=2, component_prefix="PC", random_state=None):
    """Reduce many numeric features into principal components.

    Use PCA when students have many related variables and want to visualize or
    simplify them. For example, PCA can reduce many demographic, land-use, and
    transportation access variables into two components for plotting or
    clustering.

    Parameters
    ----------
    data : dict or pandas.DataFrame
        Prepared ML dictionary from `prepare_ml_data` or a numeric feature
        table.
    n_components : int, default 2
        Number of principal components to calculate.
    component_prefix : str, default "PC"
        Prefix for component column names.
    random_state : int, optional
        Random seed for PCA solvers that use randomness.

    Returns
    -------
    dict
        Dictionary with fitted `model`, component `data`, explained variance
        ratios, and feature `loadings`.

    Example
    -------
    >>> from helper.ml import run_pca
    >>> pca_result = run_pca(ml_data, n_components=2)
    >>> pca_result["data"].head()
    """
    require_sklearn("run_pca")
    pd = require_pandas("run_pca")
    from sklearn.decomposition import PCA

    X = get_X(data)
    model = PCA(n_components=n_components, random_state=random_state)
    components = model.fit_transform(X)
    component_columns = [f"{component_prefix}{i + 1}" for i in range(n_components)]
    component_data = pd.DataFrame(components, columns=component_columns, index=getattr(X, "index", None))

    feature_names = safe_feature_names(X)
    loadings = pd.DataFrame(
        model.components_.T,
        index=feature_names,
        columns=component_columns,
    )
    loadings.index.name = "feature"
    loadings = loadings.reset_index()

    return {
        "model": model,
        "data": component_data,
        "explained_variance_ratio": model.explained_variance_ratio_,
        "loadings": loadings,
    }
