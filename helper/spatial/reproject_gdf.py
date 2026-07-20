"""Reproject a GeoDataFrame to a new CRS."""


def reproject_gdf(gdf, epsg):
    """Reproject a GeoDataFrame to another EPSG code.

    Use this when two spatial datasets have different CRS values or when a
    dataset must be projected before measuring distance or area.

    Parameters
    ----------
    gdf : geopandas.GeoDataFrame
        The spatial dataset to reproject.
    epsg : int
        The target EPSG code. For example, 4326 is WGS84 longitude/latitude.

    Returns
    -------
    geopandas.GeoDataFrame
        A new GeoDataFrame in the requested CRS.

    Example
    -------
    >>> from helper.data_read import read_geojson_file
    >>> from helper.spatial import reproject_gdf
    >>> trails = read_geojson_file("data/trails_dallas_county/Trails_ Off-Street, Existing.geojson")
    >>> trails_4326 = reproject_gdf(trails, 4326)
    """
    try:
        import geopandas as gpd
    except ImportError as exc:
        raise ImportError(
            "geopandas is required for spatial helpers. Install it with: pip install geopandas"
        ) from exc

    if not isinstance(gdf, gpd.GeoDataFrame):
        raise TypeError("reproject_gdf expects a geopandas GeoDataFrame.")

    if gdf.crs is None:
        raise ValueError("This GeoDataFrame has no CRS. Set it first with gdf.set_crs(...).")

    return gdf.to_crs(epsg=epsg)
