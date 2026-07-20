"""Explain fitted model results with metrics, errors, and importance."""

from ._ml_helpers import require_pandas, require_sklearn, safe_feature_names
from .evaluate_classification import evaluate_classification
from .evaluate_regression import evaluate_regression
from .get_feature_importance import get_feature_importance


def _infer_task_type(y):
    """Infer a likely task type from y."""
    pd = require_pandas("explain_model_results")
    series = pd.Series(y).dropna()
    if pd.api.types.is_numeric_dtype(series) and series.nunique() > 10:
        return "regression"
    return "classification"


def _permutation_importance_table(
    model,
    X,
    y,
    feature_names,
    n_repeats,
    random_state,
    scoring,
    top_n,
):
    """Return a tidy permutation importance table."""
    require_sklearn("explain_model_results")
    pd = require_pandas("explain_model_results")
    from sklearn.inspection import permutation_importance

    result = permutation_importance(
        model,
        X,
        y,
        n_repeats=n_repeats,
        random_state=random_state,
        scoring=scoring,
    )
    output = pd.DataFrame(
        {
            "feature": safe_feature_names(X, feature_names),
            "importance_mean": result.importances_mean,
            "importance_std": result.importances_std,
        }
    ).sort_values("importance_mean", ascending=False)
    if top_n is not None:
        output = output.head(top_n)
    return output.reset_index(drop=True)


def explain_model_results(
    model,
    X,
    y=None,
    task_type="auto",
    feature_names=None,
    top_n=15,
    include_permutation=True,
    n_repeats=5,
    random_state=42,
    scoring=None,
):
    """Explain a fitted supervised model in a student-friendly bundle.

    The output combines three ideas students should discuss in an AI analysis:
    overall model performance, which features seem influential, and where the
    model makes its largest errors or mistakes.

    Parameters
    ----------
    model : estimator
        Fitted scikit-learn model.
    X : pandas.DataFrame or array-like
        Feature table used for prediction or explanation.
    y : array-like, optional
        Observed values. When provided, metrics and error tables are returned.
    task_type : {"auto", "regression", "classification"}, default "auto"
        Type of supervised model.
    feature_names : list, optional
        Names of features when `X` is not a DataFrame.
    top_n : int or None, default 15
        Number of importance/error rows to return.
    include_permutation : bool, default True
        If True and `y` is provided, calculate permutation importance.
    n_repeats : int, default 5
        Number of permutation repeats.
    random_state : int, default 42
        Random seed for permutation importance.
    scoring : str or callable, optional
        Scikit-learn scoring value for permutation importance.

    Returns
    -------
    dict
        Dictionary with `metrics`, `feature_importance`,
        `permutation_importance`, `predictions`, and `error_table` when
        available.

    Example
    -------
    >>> from helper.ml import explain_model_results
    >>> explanation = explain_model_results(best_model, X_test, y_test)
    >>> explanation["feature_importance"]
    """
    require_sklearn("explain_model_results")
    pd = require_pandas("explain_model_results")

    if task_type == "auto":
        if y is None:
            task_type = "regression"
        else:
            task_type = _infer_task_type(y)
    task_type = str(task_type).lower()
    if task_type not in {"regression", "classification"}:
        raise ValueError("task_type must be 'auto', 'regression', or 'classification'.")

    predictions = model.predict(X)
    output = {
        "task_type": task_type,
        "predictions": predictions,
        "metrics": None,
        "feature_importance": None,
        "permutation_importance": None,
        "error_table": None,
    }

    try:
        output["feature_importance"] = get_feature_importance(
            model,
            feature_names=safe_feature_names(X, feature_names),
            top_n=top_n,
        )
    except ValueError:
        output["feature_importance"] = None

    if y is None:
        return output

    y_series = pd.Series(y).reset_index(drop=True)
    pred_series = pd.Series(predictions).reset_index(drop=True)

    if task_type == "regression":
        output["metrics"] = evaluate_regression(y_series, pred_series)
        error_table = pd.DataFrame(
            {
                "actual": y_series,
                "predicted": pred_series,
                "error": pred_series - y_series,
            }
        )
        error_table["absolute_error"] = error_table["error"].abs()
        error_table = error_table.sort_values(
            "absolute_error",
            ascending=False,
        )
        if top_n is not None:
            error_table = error_table.head(top_n)
        output["error_table"] = error_table.reset_index(drop=False).rename(
            columns={"index": "row_index"}
        )
    else:
        probabilities = model.predict_proba(X) if hasattr(model, "predict_proba") else None
        output["metrics"] = evaluate_classification(y_series, pred_series, probabilities)
        error_table = pd.DataFrame({"actual": y_series, "predicted": pred_series})
        error_table["correct"] = error_table["actual"] == error_table["predicted"]
        if probabilities is not None:
            probability_frame = pd.DataFrame(probabilities)
            error_table["prediction_confidence"] = probability_frame.max(axis=1)
            error_table = error_table.sort_values("prediction_confidence", ascending=False)
        error_table = error_table.loc[~error_table["correct"]]
        if top_n is not None:
            error_table = error_table.head(top_n)
        output["error_table"] = error_table.reset_index(drop=False).rename(
            columns={"index": "row_index"}
        )

    if include_permutation:
        output["permutation_importance"] = _permutation_importance_table(
            model,
            X,
            y,
            feature_names,
            n_repeats,
            random_state,
            scoring,
            top_n,
        )

    return output
