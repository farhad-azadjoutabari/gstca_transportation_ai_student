"""Use a fitted model for prediction."""

from ._ml_helpers import require_pandas


def predict_with_model(
    model,
    X,
    output_column="prediction",
    include_probabilities=True,
    return_dataframe=True,
):
    """Predict values or classes with a fitted model.

    Use this after training a regression or classification model to apply it
    to new records, all Census tracts, or a future scenario table.

    Parameters
    ----------
    model : estimator
        Fitted scikit-learn model with a `predict` method.
    X : pandas.DataFrame or array-like
        Feature table to predict.
    output_column : str, default "prediction"
        Name of the prediction column when returning a DataFrame.
    include_probabilities : bool, default True
        For classification models with `predict_proba`, include probability
        columns in the output DataFrame.
    return_dataframe : bool, default True
        If True, return a copy of X with prediction columns. If False, return
        only the prediction array.

    Returns
    -------
    pandas.DataFrame or array-like
        Predictions as a DataFrame or array.

    Example
    -------
    >>> from helper.ml import predict_with_model
    >>> predicted_tracts = predict_with_model(result["model"], ml_data["X"])
    """
    pd = require_pandas("predict_with_model")
    predictions = model.predict(X)
    if not return_dataframe:
        return predictions

    if hasattr(X, "copy") and hasattr(X, "columns"):
        result = X.copy()
    else:
        result = pd.DataFrame(X)

    result[output_column] = predictions

    if include_probabilities and hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(X)
        classes = getattr(model, "classes_", range(probabilities.shape[1]))
        for index, class_name in enumerate(classes):
            result[f"{output_column}_probability_{class_name}"] = probabilities[:, index]

    return result
