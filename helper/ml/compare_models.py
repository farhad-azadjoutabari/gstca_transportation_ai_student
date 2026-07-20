"""Compare a broader set of supervised machine learning models."""

from ._ml_helpers import get_split_data, require_pandas, require_sklearn
from .evaluate_classification import evaluate_classification
from .evaluate_regression import evaluate_regression


def _infer_task_type(y):
    """Infer a reasonable supervised ML task type from the target."""
    pd = require_pandas("compare_models")
    series = pd.Series(y).dropna()
    if series.empty:
        raise ValueError("Cannot infer task type from an empty target.")
    if pd.api.types.is_numeric_dtype(series) and series.nunique() > 10:
        return "regression"
    return "classification"


def _regression_model(model_type, random_state):
    """Create one regression estimator."""
    require_sklearn("compare_models")
    from sklearn.dummy import DummyRegressor
    from sklearn.ensemble import (
        ExtraTreesRegressor,
        GradientBoostingRegressor,
        HistGradientBoostingRegressor,
        RandomForestRegressor,
    )
    from sklearn.linear_model import Lasso, LinearRegression, Ridge
    from sklearn.tree import DecisionTreeRegressor

    name = str(model_type).lower().replace("-", "_").replace(" ", "_")
    if name in {"baseline", "dummy", "mean"}:
        return DummyRegressor(strategy="mean")
    if name in {"linear", "linear_regression", "ols"}:
        return LinearRegression()
    if name == "ridge":
        return Ridge()
    if name == "lasso":
        return Lasso(random_state=random_state)
    if name in {"decision_tree", "tree"}:
        return DecisionTreeRegressor(random_state=random_state)
    if name in {"random_forest", "forest"}:
        return RandomForestRegressor(n_estimators=100, random_state=random_state)
    if name in {"extra_trees", "extremely_randomized_trees"}:
        return ExtraTreesRegressor(n_estimators=100, random_state=random_state)
    if name in {"gradient_boosting", "gb"}:
        return GradientBoostingRegressor(random_state=random_state)
    if name in {"hist_gradient_boosting", "histgb", "hist_gb"}:
        return HistGradientBoostingRegressor(random_state=random_state)
    raise ValueError(f"Unknown regression model_type: {model_type}")


def _classification_model(model_type, random_state):
    """Create one classification estimator."""
    require_sklearn("compare_models")
    from sklearn.dummy import DummyClassifier
    from sklearn.ensemble import (
        ExtraTreesClassifier,
        GradientBoostingClassifier,
        HistGradientBoostingClassifier,
        RandomForestClassifier,
    )
    from sklearn.linear_model import LogisticRegression
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.svm import SVC
    from sklearn.tree import DecisionTreeClassifier

    name = str(model_type).lower().replace("-", "_").replace(" ", "_")
    if name in {"baseline", "dummy", "most_frequent"}:
        return DummyClassifier(strategy="most_frequent")
    if name in {"logistic", "logistic_regression"}:
        return LogisticRegression(max_iter=1000, random_state=random_state)
    if name in {"decision_tree", "tree"}:
        return DecisionTreeClassifier(random_state=random_state)
    if name in {"random_forest", "forest"}:
        return RandomForestClassifier(n_estimators=100, random_state=random_state)
    if name in {"extra_trees", "extremely_randomized_trees"}:
        return ExtraTreesClassifier(n_estimators=100, random_state=random_state)
    if name in {"gradient_boosting", "gb"}:
        return GradientBoostingClassifier(random_state=random_state)
    if name in {"hist_gradient_boosting", "histgb", "hist_gb"}:
        return HistGradientBoostingClassifier(random_state=random_state)
    if name in {"knn", "k_nearest_neighbors"}:
        return KNeighborsClassifier()
    if name in {"svm", "support_vector_machine"}:
        return SVC(probability=True, random_state=random_state)
    raise ValueError(f"Unknown classification model_type: {model_type}")


def compare_models(
    X_train,
    y_train=None,
    X_test=None,
    y_test=None,
    task_type="auto",
    model_types=None,
    random_state=42,
    continue_on_error=True,
):
    """Train and compare several supervised ML algorithms.

    This higher-level helper lets students spend more time on the AI question:
    which algorithm works best, whether it improves over a baseline, and what
    tradeoffs appear in the metrics. It supports both regression and
    classification and includes stronger algorithms than the smaller
    challenge-oriented comparison helpers.

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
    task_type : {"auto", "regression", "classification"}, default "auto"
        Type of supervised model comparison.
    model_types : list or None, default None
        Models to compare. If None, a broad default set is used.
    random_state : int, default 42
        Random seed for models that use randomness.
    continue_on_error : bool, default True
        If True, failed models are listed in an `errors` table instead of
        stopping the full comparison.

    Returns
    -------
    dict
        Dictionary with `task_type`, sorted `results`, fitted `models`,
        `predictions`, optional `probabilities`, and `errors`.

    Example
    -------
    >>> from helper.ml import compare_models
    >>> comparison = compare_models(split_data, task_type="regression")
    >>> comparison["results"]
    """
    require_sklearn("compare_models")
    pd = require_pandas("compare_models")

    split = get_split_data(X_train)
    if split is not None:
        X_train, X_test, y_train, y_test = split
    if y_train is None or X_test is None or y_test is None:
        raise ValueError("Training and testing features/targets are required.")

    if task_type == "auto":
        task_type = _infer_task_type(y_train)
    task_type = str(task_type).lower()
    if task_type not in {"regression", "classification"}:
        raise ValueError("task_type must be 'auto', 'regression', or 'classification'.")

    if model_types is None:
        if task_type == "regression":
            model_types = [
                "baseline",
                "linear_regression",
                "ridge",
                "lasso",
                "decision_tree",
                "random_forest",
                "extra_trees",
                "gradient_boosting",
                "hist_gradient_boosting",
            ]
        else:
            model_types = [
                "baseline",
                "logistic_regression",
                "decision_tree",
                "random_forest",
                "extra_trees",
                "gradient_boosting",
                "hist_gradient_boosting",
                "knn",
                "svm",
            ]

    rows = []
    errors = []
    models = {}
    predictions = {}
    probabilities = {}

    for model_type in model_types:
        try:
            if task_type == "regression":
                model = _regression_model(model_type, random_state)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                rows.append({"model_type": model_type, **evaluate_regression(y_test, y_pred)})
                models[model_type] = model
                predictions[model_type] = y_pred
            else:
                model = _classification_model(model_type, random_state)
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
        except Exception as exc:
            if not continue_on_error:
                raise
            errors.append({"model_type": model_type, "error": str(exc)})

    results = pd.DataFrame(rows)
    if not results.empty:
        if task_type == "regression":
            results = results.sort_values(["rmse", "mae"]).reset_index(drop=True)
        else:
            results = results.sort_values(["f1_macro", "accuracy"], ascending=False).reset_index(drop=True)

    return {
        "task_type": task_type,
        "results": results,
        "models": models,
        "predictions": predictions,
        "probabilities": probabilities,
        "errors": pd.DataFrame(errors),
    }
