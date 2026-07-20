"""Summarize a GeoDataFrame."""


def summarize_gdf(gdf):
    """Return a quick summary of a GeoDataFrame.

    Use this function right after reading a shapefile, GeoJSON, or GeoPackage
    to understand what is inside the dataset before doing analysis.

    Parameters
    ----------
    gdf : geopandas.GeoDataFrame
        The spatial dataset to summarize.

    Returns
    -------
    dict
        A dictionary with row count, column count, column names, CRS,
        geometry types, missing values, empty geometries, and map bounds.

    Example
    -------
    >>> from helper.data_read import read_shp_file
    >>> from helper.spatial import summarize_gdf
    >>> airports = read_shp_file("data/existing_airport_dfw/Existing_Airports.shp")
    >>> summary = summarize_gdf(airports)
    >>> summary["row_count"]
    195
    """
    try:
        import geopandas as gpd
    except ImportError as exc:
        raise ImportError(
            "geopandas is required for spatial helpers. Install it with: pip install geopandas"
        ) from exc

    if not isinstance(gdf, gpd.GeoDataFrame):
        raise TypeError("summarize_gdf expects a geopandas GeoDataFrame.")

    geometry = gdf.geometry
    geometry_types = {
        name: int(count)
        for name, count in geometry.geom_type.fillna("Missing").value_counts().items()
    }
    missing_values = gdf.isna().sum().astype(int).to_dict()
    empty_geometry_count = int((geometry.notna() & geometry.is_empty).sum())
    bounds = None if gdf.empty else dict(zip(["minx", "miny", "maxx", "maxy"], gdf.total_bounds))

    return {
        "row_count": int(len(gdf)),
        "column_count": int(len(gdf.columns)),
        "columns": list(gdf.columns),
        "geometry_column": gdf.geometry.name,
        "crs": str(gdf.crs) if gdf.crs is not None else None,
        "geometry_types": geometry_types,
        "missing_values": missing_values,
        "missing_geometry_count": int(geometry.isna().sum()),
        "empty_geometry_count": empty_geometry_count,
        "bounds": bounds,
    }
