"""Check the coordinate reference system of a GeoDataFrame."""


def check_crs(gdf):
    """Return useful information about a GeoDataFrame's CRS.

    CRS means coordinate reference system. Students should check it before
    measuring distance, area, or combining two spatial datasets. A geographic
    CRS usually stores coordinates as longitude and latitude. A projected CRS
    is usually better for measuring distance and area.

    Parameters
    ----------
    gdf : geopandas.GeoDataFrame
        The spatial dataset to inspect.

    Returns
    -------
    dict
        CRS details including EPSG code, whether it is geographic or projected,
        and the coordinate unit when available.

    Example
    -------
    >>> from helper.data_read import read_shp_file
    >>> from helper.spatial import check_crs
    >>> roads = read_shp_file("data/dfw_truck_lane_restriction/Truck_Lane_Restrictions.shp")
    >>> crs_info = check_crs(roads)
    >>> crs_info["is_projected"]
    True
    """
    try:
        import geopandas as gpd
    except ImportError as exc:
        raise ImportError(
            "geopandas is required for spatial helpers. Install it with: pip install geopandas"
        ) from exc

    if not isinstance(gdf, gpd.GeoDataFrame):
        raise TypeError("check_crs expects a geopandas GeoDataFrame.")

    crs = gdf.crs
    if crs is None:
        return {
            "crs": None,
            "epsg": None,
            "is_geographic": None,
            "is_projected": None,
            "unit": None,
            "message": "This GeoDataFrame does not have a CRS assigned.",
        }

    unit = None
    if crs.axis_info:
        unit = crs.axis_info[0].unit_name

    return {
        "crs": str(crs),
        "epsg": crs.to_epsg(),
        "is_geographic": bool(crs.is_geographic),
        "is_projected": bool(crs.is_projected),
        "unit": unit,
        "message": "Projected CRS is best for distance and area." if crs.is_projected else "Geographic CRS is best for mapping, not measurement.",
    }
