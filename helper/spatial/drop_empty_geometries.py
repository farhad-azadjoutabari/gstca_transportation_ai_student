"""Remove rows with missing or empty geometries."""


def drop_empty_geometries(gdf, reset_index=True):
    """Drop rows where the geometry is missing or empty.

    Missing or empty geometries can break maps, spatial joins, clipping,
    buffering, and distance calculations. This helper returns a cleaned copy
    of the GeoDataFrame.

    Parameters
    ----------
    gdf : geopandas.GeoDataFrame
        The spatial dataset to clean.
    reset_index : bool, default True
        If True, reset the row index after dropping rows.

    Returns
    -------
    geopandas.GeoDataFrame
        A copy of the input with only valid, non-empty geometry rows.

    Example
    -------
    >>> from helper.data_read import read_shp_file
    >>> from helper.spatial import drop_empty_geometries
    >>> signs = read_shp_file("data/traffic_signs_city_of_dallas/TrafficSigns.shp")
    >>> signs_clean = drop_empty_geometries(signs)
    """
    try:
        import geopandas as gpd
    except ImportError as exc:
        raise ImportError(
            "geopandas is required for spatial helpers. Install it with: pip install geopandas"
        ) from exc

    if not isinstance(gdf, gpd.GeoDataFrame):
        raise TypeError("drop_empty_geometries expects a geopandas GeoDataFrame.")

    keep_rows = gdf.geometry.notna() & ~gdf.geometry.is_empty
    cleaned = gdf.loc[keep_rows].copy()

    if reset_index:
        cleaned = cleaned.reset_index(drop=True)

    return cleaned
