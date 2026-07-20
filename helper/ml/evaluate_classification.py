"""Evaluate classification predictions."""

from ._ml_helpers import require_pandas, require_sklearn


def evaluate_classification(y_true, y_pred, y_prob=None, labels=None):
    """Calculate common classification accuracy metrics.

    Use this after predicting categories to understand where the model is
    correct or wrong. The confusion matrix shows which classes are confused
    with each other.

    Parameters
    ----------
    y_true : array-like
        Observed class labels.
    y_pred : array-like
        Predicted class labels.
    y_prob : array-like, optional
        Predicted class probabilities from `predict_proba`.
    labels : list, optional
        Class labels to use in the confusion matrix.

    Returns
    -------
    dict
        Dictionary with accuracy, precision, recall, F1, optional ROC-AUC,
        a confusion matrix DataFrame, and a classification report DataFrame.

    Example
    -------
    >>> from helper.ml import evaluate_classification
    >>> metrics = evaluate_classification(result["y_test"], result["predictions"])
    """
    require_sklearn("evaluate_classification")
    pd = require_pandas("evaluate_classification")
    from sklearn.metrics import (
        accuracy_score,
        classification_report,
        confusion_matrix,
        f1_score,
        precision_score,
        recall_score,
        roc_auc_score,
    )

    if labels is None:
        labels = sorted(pd.Series(y_true).dropna().unique())

    metrics = {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision_macro": precision_score(y_true, y_pred, average="macro", zero_division=0),
        "recall_macro": recall_score(y_true, y_pred, average="macro", zero_division=0),
        "f1_macro": f1_score(y_true, y_pred, average="macro", zero_division=0),
        "roc_auc": None,
    }

    if y_prob is not None:
        try:
            if len(labels) == 2:
                probability_values = y_prob[:, 1] if getattr(y_prob, "ndim", 1) > 1 else y_prob
                metrics["roc_auc"] = roc_auc_score(y_true, probability_values)
            else:
                metrics["roc_auc"] = roc_auc_score(y_true, y_prob, multi_class="ovr")
        except Exception:
            metrics["roc_auc"] = None

    matrix = confusion_matrix(y_true, y_pred, labels=labels)
    metrics["confusion_matrix"] = pd.DataFrame(matrix, index=labels, columns=labels)
    metrics["classification_report"] = pd.DataFrame(
        classification_report(y_true, y_pred, zero_division=0, output_dict=True)
    ).transpose()

    return metrics
