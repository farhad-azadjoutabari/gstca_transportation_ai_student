"""Internal helpers for machine learning functions."""


def require_sklearn(function_name):
    """Raise a friendly error if scikit-learn is not installed."""
    try:
        import sklearn  # noqa: F401
    except ImportError as exc:
        raise ImportError(
            f"scikit-learn is required for {function_name}. Install it with: pip install scikit-learn"
        ) from exc


def require_pandas(function_name):
    """Return pandas with a friendly installation message."""
    try:
        import pandas as pd
    except ImportError as exc:
        raise ImportError(
            f"pandas is required for {function_name}. Install it with: pip install pandas"
        ) from exc
    return pd


def normalize_columns(columns, parameter_name):
    """Convert a string or iterable of column names into a list."""
    if columns is None:
        return []
    if isinstance(columns, str):
        return [columns]
    try:
        return list(columns)
    except TypeError as exc:
        raise TypeError(f"{parameter_name} must be a string, list, or tuple of column names.") from exc


def check_columns(df, columns, parameter_name):
    """Check that all requested columns exist in a DataFrame."""
    missing = [column for column in columns if column not in df.columns]
    if missing:
        raise ValueError(f"{parameter_name} contains columns that were not found: {missing}")


def get_X(data):
    """Extract feature data from a prepared ML dictionary or return data itself."""
    if isinstance(data, dict) and "X" in data:
        return data["X"]
    return data


def get_y(data, y=None):
    """Extract target data from a prepared ML dictionary or return y."""
    if y is not None:
        return y
    if isinstance(data, dict) and "y" in data:
        return data["y"]
    return None


def get_split_data(data):
    """Extract train/test arrays from a split dictionary."""
    if not isinstance(data, dict):
        return None

    required = {"X_train", "X_test", "y_train", "y_test"}
    if required <= set(data):
        return data["X_train"], data["X_test"], data["y_train"], data["y_test"]

    return None


def result_dataframe(X, output_column, values):
    """Return a DataFrame copy of X with one output column added."""
    pd = require_pandas("machine learning result helpers")
    if hasattr(X, "copy") and hasattr(X, "columns"):
        result = X.copy()
    else:
        result = pd.DataFrame(X)
    result[output_column] = values
    return result


def get_regression_model(model_type="random_forest", random_state=42, **model_kwargs):
    """Create a regression model from a student-friendly model name."""
    require_sklearn("get_regression_model")
    from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
    from sklearn.linear_model import Lasso, LinearRegression, Ridge
    from sklearn.tree import DecisionTreeRegressor

    name = str(model_type).lower().replace("-", "_").replace(" ", "_")
    aliases = {
        "linear": "linear_regression",
        "ols": "linear_regression",
        "decision_tree": "decision_tree",
        "tree": "decision_tree",
        "random_forest": "random_forest",
        "forest": "random_forest",
        "gradient_boosting": "gradient_boosting",
        "gb": "gradient_boosting",
    }
    name = aliases.get(name, name)

    if name == "linear_regression":
        return LinearRegression(**model_kwargs)
    if name == "ridge":
        return Ridge(**model_kwargs)
    if name == "lasso":
        return Lasso(random_state=random_state, **model_kwargs)
    if name == "decision_tree":
        return DecisionTreeRegressor(random_state=random_state, **model_kwargs)
    if name == "random_forest":
        model_kwargs.setdefault("n_estimators", 100)
        return RandomForestRegressor(random_state=random_state, **model_kwargs)
    if name == "gradient_boosting":
        return GradientBoostingRegressor(random_state=random_state, **model_kwargs)

    raise ValueError(
        "model_type must be one of: linear_regression, ridge, lasso, "
        "decision_tree, random_forest, gradient_boosting."
    )


def get_classification_model(model_type="random_forest", random_state=42, **model_kwargs):
    """Create a classification model from a student-friendly model name."""
    require_sklearn("get_classification_model")
    from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.svm import SVC
    from sklearn.tree import DecisionTreeClassifier

    name = str(model_type).lower().replace("-", "_").replace(" ", "_")
    aliases = {
        "logistic": "logistic_regression",
        "decision_tree": "decision_tree",
        "tree": "decision_tree",
        "random_forest": "random_forest",
        "forest": "random_forest",
        "gradient_boosting": "gradient_boosting",
        "gb": "gradient_boosting",
        "knn": "knn",
        "k_nearest_neighbors": "knn",
        "svm": "svm",
        "support_vector_machine": "svm",
    }
    name = aliases.get(name, name)

    if name == "logistic_regression":
        model_kwargs.setdefault("max_iter", 1000)
        return LogisticRegression(random_state=random_state, **model_kwargs)
    if name == "decision_tree":
        return DecisionTreeClassifier(random_state=random_state, **model_kwargs)
    if name == "random_forest":
        model_kwargs.setdefault("n_estimators", 100)
        return RandomForestClassifier(random_state=random_state, **model_kwargs)
    if name == "gradient_boosting":
        return GradientBoostingClassifier(random_state=random_state, **model_kwargs)
    if name == "knn":
        return KNeighborsClassifier(**model_kwargs)
    if name == "svm":
        model_kwargs.setdefault("probability", True)
        return SVC(random_state=random_state, **model_kwargs)

    raise ValueError(
        "model_type must be one of: logistic_regression, decision_tree, "
        "random_forest, gradient_boosting, knn, svm."
    )


def safe_feature_names(X, feature_names=None):
    """Return feature names for arrays or DataFrames."""
    if feature_names is not None:
        return list(feature_names)
    if hasattr(X, "columns"):
        return list(X.columns)
    try:
        return [f"feature_{i}" for i in range(X.shape[1])]
    except Exception:
        return []
