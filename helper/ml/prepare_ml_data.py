"""Prepare tabular data for machine learning."""

from ._ml_helpers import check_columns, normalize_columns, require_pandas, require_sklearn


def prepare_ml_data(
    df,
    feature_columns,
    target_column=None,
    numeric_columns=None,
    categorical_columns=None,
    scale_numeric=True,
    drop_missing_target=True,
):
    """Prepare features and an optional target column for machine learning.

    Use this after students finish cleaning, joining, and summarizing their
    data. The function selects feature columns, handles missing feature values,
    converts categorical columns into numeric dummy variables, and optionally
    scales numeric columns. The output can be passed directly to clustering,
    regression, classification, or PCA helpers.

    Parameters
    ----------
    df : pandas.DataFrame
        Table containing the variables to model. A GeoDataFrame also works,
        but do not include the geometry column in `feature_columns`.
    feature_columns : list
        Columns used as model inputs.
    target_column : str, optional
        Column students want to predict. Leave as None for clustering or PCA.
    numeric_columns : list, optional
        Feature columns that should be treated as numeric. If None, numeric
        columns are detected automatically.
    categorical_columns : list, optional
        Feature columns that should be one-hot encoded. If None, text,
        category, and boolean columns are treated as categorical.
    scale_numeric : bool, default True
        Whether to standardize numeric features. This is helpful for K-Means,
        DBSCAN, KNN, SVM, PCA, and regularized regression.
    drop_missing_target : bool, default True
        Whether to drop rows with missing target values when `target_column`
        is provided.

    Returns
    -------
    dict
        Dictionary with prepared `X`, optional `y`, the fitted `preprocessor`,
        selected columns, and the original rows used for modeling.

    Example
    -------
    >>> from helper.ml import prepare_ml_data
    >>> ml_data = prepare_ml_data(
    ...     tracts,
    ...     feature_columns=["population", "bus_stop_count", "total_employees"],
    ...     target_column="crash_count",
    ... )
    >>> X = ml_data["X"]
    >>> y = ml_data["y"]
    """
    require_sklearn("prepare_ml_data")
    pd = require_pandas("prepare_ml_data")
    from sklearn.compose import ColumnTransformer
    from sklearn.impute import SimpleImputer
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import OneHotEncoder, StandardScaler

    feature_columns = normalize_columns(feature_columns, "feature_columns")
    if not feature_columns:
        raise ValueError("feature_columns must contain at least one column.")
    check_columns(df, feature_columns, "feature_columns")

    if target_column is not None and target_column not in df.columns:
        raise ValueError(f"target_column was not found: {target_column}")

    work_df = df.copy()
    if target_column is not None and drop_missing_target:
        work_df = work_df.loc[work_df[target_column].notna()].copy()

    raw_X = work_df[feature_columns].copy()
    y = work_df[target_column].copy() if target_column is not None else None

    if numeric_columns is None and categorical_columns is None:
        categorical_columns = [
            column
            for column in feature_columns
            if (
                pd.api.types.is_object_dtype(raw_X[column])
                or pd.api.types.is_categorical_dtype(raw_X[column])
                or pd.api.types.is_bool_dtype(raw_X[column])
            )
        ]
        numeric_columns = [column for column in feature_columns if column not in categorical_columns]
    else:
        numeric_columns = normalize_columns(numeric_columns, "numeric_columns")
        categorical_columns = normalize_columns(categorical_columns, "categorical_columns")
        check_columns(raw_X, numeric_columns, "numeric_columns")
        check_columns(raw_X, categorical_columns, "categorical_columns")

    transformers = []
    if numeric_columns:
        numeric_steps = [("imputer", SimpleImputer(strategy="median"))]
        if scale_numeric:
            numeric_steps.append(("scaler", StandardScaler()))
        transformers.append(("numeric", Pipeline(numeric_steps), numeric_columns))

    if categorical_columns:
        try:
            encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
        except TypeError:
            encoder = OneHotEncoder(handle_unknown="ignore", sparse=False)
        categorical_steps = [
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", encoder),
        ]
        transformers.append(("categorical", Pipeline(categorical_steps), categorical_columns))

    if not transformers:
        raise ValueError("No numeric or categorical feature columns were selected.")

    preprocessor = ColumnTransformer(transformers=transformers, remainder="drop")
    X_values = preprocessor.fit_transform(raw_X)
    if hasattr(X_values, "toarray"):
        X_values = X_values.toarray()

    try:
        output_columns = list(preprocessor.get_feature_names_out())
        output_columns = [
            column.replace("numeric__", "").replace("categorical__", "")
            for column in output_columns
        ]
    except Exception:
        output_columns = [f"feature_{i}" for i in range(X_values.shape[1])]

    X = pd.DataFrame(X_values, columns=output_columns, index=raw_X.index)

    return {
        "X": X,
        "y": y,
        "raw_X": raw_X,
        "data": work_df,
        "preprocessor": preprocessor,
        "feature_columns": feature_columns,
        "target_column": target_column,
        "numeric_columns": numeric_columns,
        "categorical_columns": categorical_columns,
    }
