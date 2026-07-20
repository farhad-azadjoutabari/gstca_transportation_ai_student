"""Clip spatial features to a boundary."""


def clip_to_boundary(gdf, boundary_gdf):
    """Keep only features that fall inside a boundary dataset.

    Use this when students want to limit a dataset to a study area such as a
    city, county, census tract, neighborhood, or project boundary. If both
    datasets have CRS values and they differ, the boundary is reprojected to
    match the input dataset.

    Parameters
    ----------
    gdf : geopandas.GeoDataFrame
        The spatial dataset to clip.
    boundary_gdf : geopandas.GeoDataFrame
        Polygon boundary used to clip the data.

    Returns
    -------
    geopandas.GeoDataFrame
        Features from `gdf` that intersect the boundary.

    Example
    -------
    >>> from helper.data_read import read_shp_file
    >>> from helper.spatial import clip_to_boundary
    >>> roads = read_shp_file("data/speed_limits_city_of_dallas/Speed_Limits.shp")
    >>> boundary = read_shp_file("data/school_zones_city_of_dallas/School_Zones.shp")
    >>> roads_near_schools = clip_to_boundary(roads, boundary)
    """
    try:
        import geopandas as gpd
    except ImportError as exc:
        raise ImportError(
            "geopandas is required for spatial helpers. Install it with: pip install geopandas"
        ) from exc

    if not isinstance(gdf, gpd.GeoDataFrame):
        raise TypeError("clip_to_boundary expects gdf to be a geopandas GeoDataFrame.")
    if not isinstance(boundary_gdf, gpd.GeoDataFrame):
        raise TypeError("clip_to_boundary expects boundary_gdf to be a geopandas GeoDataFrame.")

    if (gdf.crs is None) != (boundary_gdf.crs is None):
        raise ValueError("Both GeoDataFrames need CRS values, or both should have no CRS.")

    boundary = boundary_gdf
    if gdf.crs is not None and boundary.crs is not None and gdf.crs != boundary.crs:
        boundary = boundary.to_crs(gdf.crs)

    return gpd.clip(gdf, boundary)
