"""Split data into training and testing sets."""

from ._ml_helpers import check_columns, get_X, get_y, require_sklearn


def split_train_test(
    data,
    y=None,
    target_column=None,
    test_size=0.2,
    random_state=42,
    stratify=None,
):
    """Split features and target values into train and test sets.

    Use this before regression or classification. Students can pass the
    dictionary returned by `prepare_ml_data`, or pass a feature table and target
    values separately.

    Parameters
    ----------
    data : dict or pandas.DataFrame
        Either the dictionary from `prepare_ml_data`, a feature table, or a
        full DataFrame when `target_column` is provided.
    y : array-like, optional
        Target values when `data` is only a feature table.
    target_column : str, optional
        Target column to separate from `data` when passing a full DataFrame.
    test_size : float, default 0.2
        Share of rows held out for testing.
    random_state : int, default 42
        Random seed for reproducible splits.
    stratify : array-like, str, or None, default None
        Values used to preserve class proportions. For classification, pass
        the target column name or target values.

    Returns
    -------
    dict
        Dictionary containing `X_train`, `X_test`, `y_train`, and `y_test`.

    Example
    -------
    >>> from helper.ml import prepare_ml_data, split_train_test
    >>> ml_data = prepare_ml_data(tracts, features, target_column="high_crash")
    >>> split_data = split_train_test(ml_data, stratify=ml_data["y"])
    """
    require_sklearn("split_train_test")
    from sklearn.model_selection import train_test_split

    if target_column is not None:
        if target_column not in data.columns:
            raise ValueError(f"target_column was not found: {target_column}")
        X = data.drop(columns=target_column)
        y_values = data[target_column]
    else:
        X = get_X(data)
        y_values = get_y(data, y)

    if y_values is None:
        raise ValueError("A target column or y values are required for train/test splitting.")

    stratify_values = stratify
    if isinstance(stratify, str):
        if isinstance(data, dict) and stratify == "y":
            stratify_values = data["y"]
        else:
            check_columns(data, [stratify], "stratify")
            stratify_values = data[stratify]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y_values,
        test_size=test_size,
        random_state=random_state,
        stratify=stratify_values,
    )

    return {
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,
    }
