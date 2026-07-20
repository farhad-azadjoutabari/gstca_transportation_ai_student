"""Internal helpers used by spatial join summary functions."""


def require_geodataframes(function_name, **items):
    """Validate that each item is a GeoDataFrame and return geopandas."""
    try:
        import geopandas as gpd
    except ImportError as exc:
        raise ImportError(
            "geopandas is required for spatial helpers. Install it with: pip install geopandas"
        ) from exc

    for name, value in items.items():
        if not isinstance(value, gpd.GeoDataFrame):
            raise TypeError(f"{function_name} expects {name} to be a geopandas GeoDataFrame.")

    return gpd


def align_crs(left_gdf, right_gdf):
    """Return right_gdf in left_gdf's CRS when both datasets have CRS values."""
    if (left_gdf.crs is None) != (right_gdf.crs is None):
        raise ValueError("Both GeoDataFrames need CRS values, or both should have no CRS.")

    if left_gdf.crs is not None and right_gdf.crs is not None and left_gdf.crs != right_gdf.crs:
        return right_gdf.to_crs(left_gdf.crs)

    return right_gdf


def prepare_measurement_crs(left_gdf, right_gdf, projected_epsg, measurement_name):
    """Project two GeoDataFrames before length or area overlap calculations."""
    if left_gdf.crs is None or right_gdf.crs is None:
        raise ValueError("Both GeoDataFrames need CRS values for overlap calculations.")

    if projected_epsg is not None:
        left = left_gdf.to_crs(epsg=projected_epsg)
        right = right_gdf.to_crs(epsg=projected_epsg)
    else:
        left = left_gdf
        right = right_gdf.to_crs(left_gdf.crs) if left_gdf.crs != right_gdf.crs else right_gdf

    if left.crs is not None and left.crs.is_geographic:
        raise ValueError(f"{measurement_name} should use a projected CRS. Pass projected_epsg.")

    return left, right


def crs_axis_factor(crs):
    """Return the conversion factor from CRS map units to meters."""
    if crs is None or not crs.axis_info:
        return 1.0

    factor = crs.axis_info[0].unit_conversion_factor
    return factor if factor else 1.0


def geometry_length_in_meters(gdf):
    """Measure geometry length in meters for a projected GeoDataFrame."""
    return gdf.geometry.length * crs_axis_factor(gdf.crs)


def geometry_area_in_square_meters(gdf):
    """Measure geometry area in square meters for a projected GeoDataFrame."""
    factor = crs_axis_factor(gdf.crs)
    return gdf.geometry.area * (factor**2)


def unique_temp_column(columns, base_name):
    """Create a temporary column name that is not already used."""
    name = base_name
    while name in columns:
        name = f"_{name}"
    return name


def list_columns(columns, available_columns, parameter_name):
    """Normalize a string/list column parameter and validate column names."""
    if columns is None:
        return list(available_columns)
    if isinstance(columns, str):
        selected = [columns]
    else:
        selected = list(columns)

    missing = [column for column in selected if column not in available_columns]
    if missing:
        raise ValueError(f"{parameter_name} contains columns that were not found: {missing}")

    return selected


def output_column_names(columns, existing_columns, prefix="", collision_suffix="_joined"):
    """Choose output column names without overwriting existing columns."""
    used = set(existing_columns)
    names = {}

    for column in columns:
        output = f"{prefix}{column}"
        if output in used:
            output = f"{output}{collision_suffix}"

        base_output = output
        counter = 2
        while output in used:
            output = f"{base_output}_{counter}"
            counter += 1

        names[column] = output
        used.add(output)

    return names


def unit_to_meters(unit):
    """Return the number of meters in one requested length unit."""
    units = {
        "meters": 1.0,
        "kilometers": 1000.0,
        "feet": 0.3048,
        "miles": 1609.344,
    }
    if unit not in units:
        raise ValueError("unit must be one of: meters, kilometers, feet, miles.")
    return units[unit]


def unit_to_square_meters(unit):
    """Return the number of square meters in one requested area unit."""
    units = {
        "square_meters": 1.0,
        "square_kilometers": 1000000.0,
        "square_feet": 0.09290304,
        "square_miles": 2589988.110336,
        "acres": 4046.8564224,
    }
    if unit not in units:
        raise ValueError(
            "unit must be one of: square_meters, square_kilometers, square_feet, square_miles, acres."
        )
    return units[unit]


def safe_column_suffix(value):
    """Convert a category value into a simple column-name suffix."""
    import re

    suffix = re.sub(r"[^0-9a-zA-Z]+", "_", str(value).strip().lower()).strip("_")
    return suffix or "missing"
