"""Internal helpers for spatial accessibility functions."""


def normalize_sum_columns(sum_columns, available_columns):
    """Normalize a sum-column parameter to an input-to-output mapping."""
    if sum_columns is None:
        return {}
    if isinstance(sum_columns, str):
        mapping = {sum_columns: f"sum_{sum_columns}"}
    elif isinstance(sum_columns, dict):
        mapping = dict(sum_columns)
    else:
        mapping = {column: f"sum_{column}" for column in sum_columns}

    missing = [column for column in mapping if column not in available_columns]
    if missing:
        raise ValueError(f"sum_columns contains columns that were not found: {missing}")

    return mapping


def normalize_selected_columns(columns, available_columns, parameter_name):
    """Normalize an optional column parameter without selecting all by default."""
    if columns is None:
        return []
    if isinstance(columns, str):
        selected = [columns]
    else:
        selected = list(columns)

    missing = [column for column in selected if column not in available_columns]
    if missing:
        raise ValueError(f"{parameter_name} contains columns that were not found: {missing}")

    return selected


def set_analysis_geometry(gdf, source_geometry, function_name):
    """Optionally replace feature geometry with a point used for distance summaries."""
    if source_geometry == "geometry":
        return gdf

    result = gdf.copy()
    geometry_column = result.geometry.name

    if source_geometry == "centroid":
        result[geometry_column] = result.geometry.centroid
    elif source_geometry == "representative_point":
        result[geometry_column] = result.geometry.representative_point()
    else:
        raise ValueError(
            f"{function_name} source_geometry must be one of: geometry, centroid, representative_point."
        )

    return result
