"""Calculate feature areas."""


def calculate_area(gdf, column_name="area", unit="square_meters", projected_epsg=None):
    """Add an area column to a GeoDataFrame.

    Use this for polygon datasets such as parks, zones, districts, parcels,
    land use areas, or census boundaries. Area should be calculated in a
    projected CRS, not longitude/latitude. If your data is in EPSG:4326, pass
    a local projected EPSG code using `projected_epsg`.

    Parameters
    ----------
    gdf : geopandas.GeoDataFrame
        The spatial dataset with polygon geometries.
    column_name : str, default "area"
        Name of the new area column.
    unit : {"square_meters", "square_kilometers", "square_feet", "square_miles", "acres"}, default "square_meters"
        Unit for the output area values.
    projected_epsg : int, optional
        EPSG code to use temporarily for measurement.

    Returns
    -------
    geopandas.GeoDataFrame
        A copy of the input with a new area column.

    Example
    -------
    >>> from helper.data_read import read_gpkg_file
    >>> from helper.spatial import calculate_area
    >>> parks = read_gpkg_file("data/parks_dallas_county/DallasCounty-Parks.gpkg")
    >>> parks = calculate_area(parks, column_name="acres", unit="acres", projected_epsg=2276)
    """
    try:
        import geopandas as gpd
    except ImportError as exc:
        raise ImportError(
            "geopandas is required for spatial helpers. Install it with: pip install geopandas"
        ) from exc

    if not isinstance(gdf, gpd.GeoDataFrame):
        raise TypeError("calculate_area expects a geopandas GeoDataFrame.")

    unit_to_square_meters = {
        "square_meters": 1.0,
        "square_kilometers": 1000000.0,
        "square_feet": 0.09290304,
        "square_miles": 2589988.110336,
        "acres": 4046.8564224,
    }
    if unit not in unit_to_square_meters:
        raise ValueError(
            "unit must be one of: square_meters, square_kilometers, square_feet, square_miles, acres."
        )

    if gdf.crs is None:
        raise ValueError("A CRS is required for area calculations. Set one first with gdf.set_crs(...).")

    measurement_gdf = gdf.to_crs(epsg=projected_epsg) if projected_epsg is not None else gdf

    if measurement_gdf.crs is not None and measurement_gdf.crs.is_geographic:
        raise ValueError("Area should be calculated in a projected CRS. Pass projected_epsg.")

    axis_factor = 1.0
    if measurement_gdf.crs is not None and measurement_gdf.crs.axis_info:
        axis_factor = measurement_gdf.crs.axis_info[0].unit_conversion_factor

    area_square_meters = measurement_gdf.geometry.area * (axis_factor**2)
    result = gdf.copy()
    result[column_name] = area_square_meters / unit_to_square_meters[unit]

    return result
