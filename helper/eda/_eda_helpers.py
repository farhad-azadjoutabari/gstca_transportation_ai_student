"""Internal helpers for exploratory data analysis functions."""


def require_pandas(function_name):
    """Return pandas with a friendly installation message."""
    try:
        import pandas as pd
    except ImportError as exc:
        raise ImportError(
            f"pandas is required for {function_name}. Install it with: pip install pandas"
        ) from exc
    return pd


def normalize_columns(columns, df, parameter_name="columns"):
    """Return selected columns or all columns when None is provided."""
    if columns is None:
        return list(df.columns)
    if isinstance(columns, str):
        selected = [columns]
    else:
        selected = list(columns)

    missing = [column for column in selected if column not in df.columns]
    if missing:
        raise ValueError(f"{parameter_name} contains columns that were not found: {missing}")
    return selected


def numeric_columns(df, columns=None):
    """Return selected numeric columns."""
    selected = normalize_columns(columns, df)
    return list(df[selected].select_dtypes(include="number").columns)
