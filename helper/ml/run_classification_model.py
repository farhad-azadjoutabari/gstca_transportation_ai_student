"""Train a classification model."""

from ._ml_helpers import get_classification_model, get_split_data, require_sklearn


def run_classification_model(
    X_train,
    y_train=None,
    X_test=None,
    model_type="random_forest",
    random_state=42,
    **model_kwargs,
):
    """Train one classification model and optionally make test predictions.

    Use classification when students want to predict a category, such as high
    versus low crash risk, congestion class, development status, transit access
    class, or whether a tract belongs to a priority group.

    Parameters
    ----------
    X_train : dict or pandas.DataFrame
        Training features, or the dictionary returned by `split_train_test`.
    y_train : array-like, optional
        Training class labels. Not needed when `X_train` is a split
        dictionary.
    X_test : pandas.DataFrame, optional
        Test features for prediction.
    model_type : str, default "random_forest"
        Classification model. Options include "logistic_regression",
        "decision_tree", "random_forest", "gradient_boosting", "knn", and
        "svm".
    random_state : int, default 42
        Random seed for models that use randomness.
    **model_kwargs
        Extra model options passed to scikit-learn.

    Returns
    -------
    dict
        Dictionary with fitted `model`, optional class `predictions`, optional
        class `probabilities`, and model metadata.

    Example
    -------
    >>> from helper.ml import split_train_test, run_classification_model
    >>> split_data = split_train_test(ml_data, stratify=ml_data["y"])
    >>> result = run_classification_model(split_data, model_type="random_forest")
    """
    require_sklearn("run_classification_model")

    split = get_split_data(X_train)
    y_test = None
    if split is not None:
        X_train, X_test, y_train, y_test = split

    if y_train is None:
        raise ValueError("y_train is required unless X_train is a split dictionary.")

    model = get_classification_model(model_type, random_state=random_state, **model_kwargs)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test) if X_test is not None else None
    probabilities = None
    if X_test is not None and hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(X_test)

    return {
        "model": model,
        "model_type": model_type,
        "predictions": predictions,
        "probabilities": probabilities,
        "X_test": X_test,
        "y_test": y_test,
    }
