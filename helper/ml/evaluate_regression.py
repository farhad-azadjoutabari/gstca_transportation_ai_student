"""Evaluate regression predictions."""

from ._ml_helpers import require_sklearn


def evaluate_regression(y_true, y_pred):
    """Calculate common regression accuracy metrics.

    Use this after predicting a numeric value to understand how close the
    predictions are to the observed values. Lower MAE/RMSE is better, and
    higher R2 is better.

    Parameters
    ----------
    y_true : array-like
        Observed numeric values.
    y_pred : array-like
        Predicted numeric values.

    Returns
    -------
    dict
        Dictionary with MAE, MSE, RMSE, and R2.

    Example
    -------
    >>> from helper.ml import evaluate_regression
    >>> metrics = evaluate_regression(result["y_test"], result["predictions"])
    """
    require_sklearn("evaluate_regression")
    import math

    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

    mse = mean_squared_error(y_true, y_pred)
    return {
        "mae": mean_absolute_error(y_true, y_pred),
        "mse": mse,
        "rmse": math.sqrt(mse),
        "r2": r2_score(y_true, y_pred),
    }
