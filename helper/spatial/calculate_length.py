"""Calculate feature lengths."""


def calculate_length(gdf, column_name="length", unit="meters", projected_epsg=None):
    """Add a length column to a GeoDataFrame.

    Use this for line datasets such as roads, trails, rail lines, bus routes,
    or street segments. Distance should be calculated in a projected CRS, not
    longitude/latitude. If your data is in EPSG:4326, pass a local projected
    EPSG code using `projected_epsg`.

    Parameters
    ----------
    gdf : geopandas.GeoDataFrame
        The spatial dataset with line geometries.
    column_name : str, default "length"
        Name of the new length column.
    unit : {"meters", "kilometers", "feet", "miles"}, default "meters"
        Unit for the output length values.
    projected_epsg : int, optional
        EPSG code to use temporarily for measurement.

    Returns
    -------
    geopandas.GeoDataFrame
        A copy of the input with a new length column.

    Example
    -------
    >>> from helper.data_read import read_geojson_file
    >>> from helper.spatial import calculate_length
    >>> bikeways = read_geojson_file("data/bikeway_dallas_county/bikeway_onstreet_existing.geojson")
    >>> bikeways = calculate_length(bikeways, column_name="miles", unit="miles", projected_epsg=2276)
    """
    try:
        import geopandas as gpd
    except ImportError as exc:
        raise ImportError(
            "geopandas is required for spatial helpers. Install it with: pip install geopandas"
        ) from exc

    if not isinstance(gdf, gpd.GeoDataFrame):
        raise TypeError("calculate_length expects a geopandas GeoDataFrame.")

    unit_to_meters = {
        "meters": 1.0,
        "kilometers": 1000.0,
        "feet": 0.3048,
        "miles": 1609.344,
    }
    if unit not in unit_to_meters:
        raise ValueError("unit must be one of: meters, kilometers, feet, miles.")

    if gdf.crs is None:
        raise ValueError("A CRS is required for length calculations. Set one first with gdf.set_crs(...).")

    measurement_gdf = gdf.to_crs(epsg=projected_epsg) if projected_epsg is not None else gdf

    if measurement_gdf.crs is not None and measurement_gdf.crs.is_geographic:
        raise ValueError("Length should be calculated in a projected CRS. Pass projected_epsg.")

    axis_factor = 1.0
    if measurement_gdf.crs is not None and measurement_gdf.crs.axis_info:
        axis_factor = measurement_gdf.crs.axis_info[0].unit_conversion_factor

    length_meters = measurement_gdf.geometry.length * axis_factor
    result = gdf.copy()
    result[column_name] = length_meters / unit_to_meters[unit]

    return result
