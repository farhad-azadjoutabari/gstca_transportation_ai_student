"""Internal helpers for feature engineering functions."""


def require_pandas(function_name):
    """Return pandas with a friendly installation message."""
    try:
        import pandas as pd
    except ImportError as exc:
        raise ImportError(
            f"pandas is required for {function_name}. Install it with: pip install pandas"
        ) from exc
    return pd


def check_columns(df, columns, parameter_name="columns"):
    """Validate that requested columns exist."""
    if isinstance(columns, str):
        columns = [columns]
    missing = [column for column in columns if column not in df.columns]
    if missing:
        raise ValueError(f"{parameter_name} contains columns that were not found: {missing}")


def safe_divide(numerator, denominator, zero_value=None):
    """Divide two numeric Series while handling zero denominators."""
    denominator = denominator.replace(0, float("nan"))
    result = numerator / denominator
    if zero_value is not None:
        result = result.fillna(zero_value)
    return result
