"""Internal helpers for transportation functions."""


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


def weighted_count_table(df, group_columns, weight_column=None):
    """Return grouped counts or weighted sums."""
    if weight_column is None:
        return df.groupby(group_columns).size().rename("trip_count").reset_index()
    check_columns(df, [weight_column], "weight_column")
    return df.groupby(group_columns)[weight_column].sum().rename("trip_count").reset_index()
