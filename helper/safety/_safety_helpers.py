"""Internal helpers for safety analysis functions."""


def require_pandas(function_name):
    """Return pandas with a friendly installation message."""
    try:
        import pandas as pd
    except ImportError as exc:
        raise ImportError(
            f"pandas is required for {function_name}. Install it with: pip install pandas"
        ) from exc
    return pd


def require_geopandas(function_name):
    """Return geopandas with a friendly installation message."""
    try:
        import geopandas as gpd
    except ImportError as exc:
        raise ImportError(
            f"geopandas is required for {function_name}. Install it with: pip install geopandas"
        ) from exc
    return gpd


def check_columns(df, columns, parameter_name="columns"):
    """Validate that requested columns exist."""
    if isinstance(columns, str):
        columns = [columns]
    missing = [column for column in columns if column not in df.columns]
    if missing:
        raise ValueError(f"{parameter_name} contains columns that were not found: {missing}")


def unique_temp_column(columns, base_name):
    """Create a temporary column name that does not already exist."""
    name = base_name
    while name in columns:
        name = f"_{name}"
    return name
