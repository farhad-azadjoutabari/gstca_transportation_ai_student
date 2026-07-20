"""Find the nearest feature in another spatial dataset."""


def find_nearest_feature(
    source_gdf,
    target_gdf,
    distance_column="distance",
    max_distance=None,
    projected_epsg=None,
    how="left",
):
    """Find the nearest target feature for each source feature.

    Use this to answer questions like "What is the nearest transit station to
    each employer?" or "What is the nearest road segment to each crash?" The
    distance calculation should use a projected CRS. If your data is in
    longitude/latitude, pass a local projected EPSG code using `projected_epsg`.

    Parameters
    ----------
    source_gdf : geopandas.GeoDataFrame
        Features that need a nearest match.
    target_gdf : geopandas.GeoDataFrame
        Features to search for nearest neighbors.
    distance_column : str, default "distance"
        Name of the output column containing nearest distance.
    max_distance : float, optional
        Maximum search distance in the units of the projected CRS.
    projected_epsg : int, optional
        EPSG code to use temporarily for distance calculation.
    how : {"left", "inner"}, default "left"
        Join style. "left" keeps all source rows.

    Returns
    -------
    geopandas.GeoDataFrame
        Source features with columns from the nearest target feature and a
        distance column.

    Example
    -------
    >>> from helper.data_read import read_gpkg_file
    >>> from helper.spatial import find_nearest_feature
    >>> employers = read_gpkg_file("data/employers_dallas_county/DallasCounty-Employer.gpkg")
    >>> stations = read_gpkg_file("data/rail_stations_dallas_county/DallasCounty-RailStations.gpkg")
    >>> nearest_station = find_nearest_feature(employers, stations, projected_epsg=2276)
    """
    try:
        import geopandas as gpd
    except ImportError as exc:
        raise ImportError(
            "geopandas is required for spatial helpers. Install it with: pip install geopandas"
        ) from exc

    if not isinstance(source_gdf, gpd.GeoDataFrame):
        raise TypeError("find_nearest_feature expects source_gdf to be a geopandas GeoDataFrame.")
    if not isinstance(target_gdf, gpd.GeoDataFrame):
        raise TypeError("find_nearest_feature expects target_gdf to be a geopandas GeoDataFrame.")

    if source_gdf.crs is None or target_gdf.crs is None:
        raise ValueError("Both GeoDataFrames need a CRS for nearest-feature analysis.")

    original_crs = source_gdf.crs
    if projected_epsg is not None:
        source = source_gdf.to_crs(epsg=projected_epsg)
        target = target_gdf.to_crs(epsg=projected_epsg)
    else:
        source = source_gdf
        target = target_gdf.to_crs(source_gdf.crs) if source_gdf.crs != target_gdf.crs else target_gdf

    if source.crs is not None and source.crs.is_geographic:
        raise ValueError("Nearest-feature distance should use a projected CRS. Pass projected_epsg.")

    result = gpd.sjoin_nearest(
        source,
        target,
        how=how,
        max_distance=max_distance,
        distance_col=distance_column,
    )

    return result.to_crs(original_crs)
