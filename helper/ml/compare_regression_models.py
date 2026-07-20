"""Compare several regression models."""

from ._ml_helpers import get_regression_model, get_split_data, require_pandas, require_sklearn
from .evaluate_regression import evaluate_regression


def compare_regression_models(
    X_train,
    y_train=None,
    X_test=None,
    y_test=None,
    model_types=None,
    random_state=42,
):
    """Train and compare several regression models.

    Use this when students are not sure which regression algorithm works best
    for their question. The returned table makes it easy to compare models by
    MAE, RMSE, and R2.

    Parameters
    ----------
    X_train : dict or pandas.DataFrame
        Training features, or the dictionary returned by `split_train_test`.
    y_train : array-like, optional
        Training target values. Not needed when `X_train` is a split
        dictionary.
    X_test : pandas.DataFrame, optional
        Test features.
    y_test : array-like, optional
        Test target values.
    model_types : list, optional
        Regression models to compare. If None, a default set is used.
    random_state : int, default 42
        Random seed for models that use randomness.

    Returns
    -------
    dict
        Dictionary with `results` DataFrame, fitted `models`, and
        `predictions`.

    Example
    -------
    >>> from helper.ml import compare_regression_models
    >>> comparison = compare_regression_models(split_data)
    >>> comparison["results"]
    """
    require_sklearn("compare_regression_models")
    pd = require_pandas("compare_regression_models")

    split = get_split_data(X_train)
    if split is not None:
        X_train, X_test, y_train, y_test = split

    if y_train is None or X_test is None or y_test is None:
        raise ValueError("Training and testing features/targets are required.")

    if model_types is None:
        model_types = [
            "linear_regression",
            "ridge",
            "lasso",
            "decision_tree",
            "random_forest",
            "gradient_boosting",
        ]

    rows = []
    models = {}
    predictions = {}
    for model_type in model_types:
        model = get_regression_model(model_type, random_state=random_state)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        metrics = evaluate_regression(y_test, y_pred)
        rows.append({"model_type": model_type, **metrics})
        models[model_type] = model
        predictions[model_type] = y_pred

    return {
        "results": pd.DataFrame(rows).sort_values("rmse").reset_index(drop=True),
        "models": models,
        "predictions": predictions,
    }
