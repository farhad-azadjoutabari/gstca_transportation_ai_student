"""Train a regression model."""

from ._ml_helpers import get_regression_model, get_split_data, require_sklearn


def run_regression_model(
    X_train,
    y_train=None,
    X_test=None,
    model_type="random_forest",
    random_state=42,
    **model_kwargs,
):
    """Train one regression model and optionally make test predictions.

    Use regression when students want to predict a numeric outcome, such as
    crash counts, traffic volume, average speed, ridership, employment, or
    development units.

    Parameters
    ----------
    X_train : dict or pandas.DataFrame
        Training features, or the dictionary returned by `split_train_test`.
    y_train : array-like, optional
        Training target values. Not needed when `X_train` is a split
        dictionary.
    X_test : pandas.DataFrame, optional
        Test features for prediction.
    model_type : str, default "random_forest"
        Regression model. Options include "linear_regression", "ridge",
        "lasso", "decision_tree", "random_forest", and "gradient_boosting".
    random_state : int, default 42
        Random seed for models that use randomness.
    **model_kwargs
        Extra model options passed to scikit-learn.

    Returns
    -------
    dict
        Dictionary with fitted `model`, optional `predictions`, and model
        metadata.

    Example
    -------
    >>> from helper.ml import split_train_test, run_regression_model
    >>> split_data = split_train_test(ml_data)
    >>> result = run_regression_model(split_data, model_type="random_forest")
    """
    require_sklearn("run_regression_model")

    split = get_split_data(X_train)
    y_test = None
    if split is not None:
        X_train, X_test, y_train, y_test = split

    if y_train is None:
        raise ValueError("y_train is required unless X_train is a split dictionary.")

    model = get_regression_model(model_type, random_state=random_state, **model_kwargs)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test) if X_test is not None else None

    return {
        "model": model,
        "model_type": model_type,
        "predictions": predictions,
        "X_test": X_test,
        "y_test": y_test,
    }
