"""Extract model feature importance."""

from ._ml_helpers import require_pandas, safe_feature_names


def get_feature_importance(model, feature_names=None, top_n=None):
    """Return the most important variables from a fitted model.

    Use this after training a model to help students interpret patterns. Tree
    models use `feature_importances_`; linear and logistic models use
    coefficients. Not every model supports feature importance.

    Parameters
    ----------
    model : estimator
        Fitted scikit-learn model.
    feature_names : list, optional
        Names of input features. If the training data was a DataFrame, pass
        `X_train.columns`.
    top_n : int, optional
        Number of top features to return.

    Returns
    -------
    pandas.DataFrame
        Table with feature names and importance values.

    Example
    -------
    >>> from helper.ml import get_feature_importance
    >>> importance = get_feature_importance(result["model"], feature_names=ml_data["X"].columns)
    """
    pd = require_pandas("get_feature_importance")

    if hasattr(model, "feature_importances_"):
        values = model.feature_importances_
        output = pd.DataFrame(
            {
                "feature": safe_feature_names(values.reshape(1, -1), feature_names),
                "importance": values,
            }
        )
    elif hasattr(model, "coef_"):
        values = model.coef_
        if getattr(values, "ndim", 1) > 1:
            values = abs(values).mean(axis=0)
        output = pd.DataFrame(
            {
                "feature": safe_feature_names(values.reshape(1, -1), feature_names),
                "coefficient": values,
                "importance": abs(values),
            }
        )
    else:
        raise ValueError("This model does not provide feature_importances_ or coef_.")

    output = output.sort_values("importance", ascending=False).reset_index(drop=True)
    if top_n is not None:
        output = output.head(top_n)
    return output
