"""Create buffers around spatial features."""


def buffer_features(gdf, distance, projected_epsg=None):
    """Create buffer polygons around each feature.

    A buffer is an area within a given distance of a feature. For example,
    students can create a half-mile buffer around rail stations or a 500-foot
    buffer around roads. Buffer distances use the units of the projected CRS.

    Parameters
    ----------
    gdf : geopandas.GeoDataFrame
        The spatial dataset to buffer.
    distance : float
        Buffer distance in the units of the projected CRS.
    projected_epsg : int, optional
        EPSG code to use temporarily for buffering.

    Returns
    -------
    geopandas.GeoDataFrame
        A copy of the input where the geometry column contains buffer polygons.

    Example
    -------
    >>> from helper.data_read import read_gpkg_file
    >>> from helper.spatial import buffer_features
    >>> stations = read_gpkg_file("data/rail_stations_dallas_county/DallasCounty-RailStations.gpkg")
    >>> station_buffers = buffer_features(stations, distance=2640, projected_epsg=2276)
    """
    try:
        import geopandas as gpd
    except ImportError as exc:
        raise ImportError(
            "geopandas is required for spatial helpers. Install it with: pip install geopandas"
        ) from exc

    if not isinstance(gdf, gpd.GeoDataFrame):
        raise TypeError("buffer_features expects a geopandas GeoDataFrame.")

    if gdf.crs is None:
        raise ValueError("A CRS is required for buffering. Set one first with gdf.set_crs(...).")

    original_crs = gdf.crs
    work_gdf = gdf.to_crs(epsg=projected_epsg) if projected_epsg is not None else gdf.copy()

    if work_gdf.crs is not None and work_gdf.crs.is_geographic:
        raise ValueError("Buffers should be created in a projected CRS. Pass projected_epsg.")

    buffered = work_gdf.copy()
    buffered[buffered.geometry.name] = work_gdf.geometry.buffer(distance)

    if projected_epsg is not None and original_crs is not None:
        buffered = buffered.to_crs(original_crs)

    return buffered
