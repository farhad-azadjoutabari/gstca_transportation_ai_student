"""Internal helpers for similarity analysis functions."""


def require_pandas(function_name):
    """Return pandas with a friendly installation message."""
    try:
        import pandas as pd
    except ImportError as exc:
        raise ImportError(
            f"pandas is required for {function_name}. Install it with: pip install pandas"
        ) from exc
    return pd


def require_numpy(function_name):
    """Return numpy with a friendly installation message."""
    try:
        import numpy as np
    except ImportError as exc:
        raise ImportError(
            f"numpy is required for {function_name}. Install it with: pip install numpy"
        ) from exc
    return np


def check_columns(df, columns, parameter_name="columns"):
    """Validate that requested columns exist."""
    if isinstance(columns, str):
        columns = [columns]
    missing = [column for column in columns if column not in df.columns]
    if missing:
        raise ValueError(f"{parameter_name} contains columns that were not found: {missing}")


def get_record_ids(df, id_column=None):
    """Return record identifiers from an ID column or the DataFrame index."""
    if id_column is not None:
        check_columns(df, [id_column], "id_column")
        return list(df[id_column])
    return list(df.index)


def prepare_feature_matrix(df, feature_columns, scale=True):
    """Return a numeric feature matrix for similarity analysis."""
    pd = require_pandas("similarity analysis")
    np = require_numpy("similarity analysis")
    if isinstance(feature_columns, str):
        feature_columns = [feature_columns]
    check_columns(df, feature_columns, "feature_columns")

    matrix = df[feature_columns].apply(pd.to_numeric, errors="coerce")
    matrix = matrix.fillna(matrix.median(numeric_only=True))
    matrix = matrix.fillna(0)

    if scale:
        std = matrix.std().replace(0, np.nan)
        matrix = (matrix - matrix.mean()) / std
        matrix = matrix.fillna(0)

    return matrix


def pairwise_distance(matrix, metric="euclidean"):
    """Calculate a pairwise distance matrix."""
    np = require_numpy("similarity analysis")
    values = matrix.to_numpy(dtype=float)
    difference = values[:, None, :] - values[None, :, :]

    if metric == "euclidean":
        return np.sqrt((difference**2).sum(axis=2))
    if metric == "manhattan":
        return np.abs(difference).sum(axis=2)

    raise ValueError("metric must be 'euclidean' or 'manhattan'.")


def similarity_from_distance(distance):
    """Convert distance values into similarity scores from 0 to 1."""
    return 1 / (1 + distance)
