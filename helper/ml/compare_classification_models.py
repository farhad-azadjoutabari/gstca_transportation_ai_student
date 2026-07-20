"""Compare several classification models."""

from ._ml_helpers import get_classification_model, get_split_data, require_pandas, require_sklearn
from .evaluate_classification import evaluate_classification


def compare_classification_models(
    X_train,
    y_train=None,
    X_test=None,
    y_test=None,
    model_types=None,
    random_state=42,
):
    """Train and compare several classification models.

    Use this when students are not sure which classification algorithm works
    best for their question. The returned table compares accuracy, precision,
    recall, F1, and ROC-AUC when available.

    Parameters
    ----------
    X_train : dict or pandas.DataFrame
        Training features, or the dictionary returned by `split_train_test`.
    y_train : array-like, optional
        Training class labels. Not needed when `X_train` is a split
        dictionary.
    X_test : pandas.DataFrame, optional
        Test features.
    y_test : array-like, optional
        Test class labels.
    model_types : list, optional
        Classification models to compare. If None, a default set is used.
    random_state : int, default 42
        Random seed for models that use randomness.

    Returns
    -------
    dict
        Dictionary with `results` DataFrame, fitted `models`, and
        `predictions`.

    Example
    -------
    >>> from helper.ml import compare_classification_models
    >>> comparison = compare_classification_models(split_data)
    >>> comparison["results"]
    """
    require_sklearn("compare_classification_models")
    pd = require_pandas("compare_classification_models")

    split = get_split_data(X_train)
    if split is not None:
        X_train, X_test, y_train, y_test = split

    if y_train is None or X_test is None or y_test is None:
        raise ValueError("Training and testing features/targets are required.")

    if model_types is None:
        model_types = [
            "logistic_regression",
            "decision_tree",
            "random_forest",
            "gradient_boosting",
            "knn",
            "svm",
        ]

    rows = []
    models = {}
    predictions = {}
    probabilities = {}

    for model_type in model_types:
        model = get_classification_model(model_type, random_state=random_state)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test) if hasattr(model, "predict_proba") else None
        metrics = evaluate_classification(y_test, y_pred, y_prob)
        rows.append(
            {
                "model_type": model_type,
                "accuracy": metrics["accuracy"],
                "precision_macro": metrics["precision_macro"],
                "recall_macro": metrics["recall_macro"],
                "f1_macro": metrics["f1_macro"],
                "roc_auc": metrics["roc_auc"],
            }
        )
        models[model_type] = model
        predictions[model_type] = y_pred
        probabilities[model_type] = y_prob

    return {
        "results": pd.DataFrame(rows).sort_values("f1_macro", ascending=False).reset_index(drop=True),
        "models": models,
        "predictions": predictions,
        "probabilities": probabilities,
    }
