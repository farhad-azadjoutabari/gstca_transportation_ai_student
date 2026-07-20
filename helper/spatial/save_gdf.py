"""Save a GeoDataFrame to a spatial file."""

from pathlib import Path


def save_gdf(gdf, output_path, driver=None, **kwargs):
    """Save a GeoDataFrame as GeoJSON, GeoPackage, or Shapefile.

    Use this after cleaning or analyzing a dataset so students can reuse the
    result in another notebook, GIS software, or web map. The file type is
    detected from the output extension unless `driver` is provided.

    Parameters
    ----------
    gdf : geopandas.GeoDataFrame
        The spatial dataset to save.
    output_path : str or pathlib.Path
        Output file path. Supported extensions include .geojson, .json, .gpkg,
        and .shp.
    driver : str, optional
        File driver passed to GeoDataFrame.to_file. Most students can leave
        this as None.
    **kwargs
        Additional options passed to GeoDataFrame.to_file. For GeoPackage,
        students can pass layer="layer_name".

    Returns
    -------
    pathlib.Path
        Path to the saved file.

    Example
    -------
    >>> from helper.data_read import read_gpkg_file
    >>> from helper.spatial import calculate_area, save_gdf
    >>> parks = read_gpkg_file("data/parks_dallas_county/DallasCounty-Parks.gpkg")
    >>> parks = calculate_area(parks, column_name="acres", unit="acres", projected_epsg=2276)
    >>> output_path = save_gdf(parks, "outputs/parks_with_area.geojson")
    """
    try:
        import geopandas as gpd
    except ImportError as exc:
        raise ImportError(
            "geopandas is required for spatial helpers. Install it with: pip install geopandas"
        ) from exc

    if not isinstance(gdf, gpd.GeoDataFrame):
        raise TypeError("save_gdf expects a geopandas GeoDataFrame.")

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    if driver is None:
        drivers_by_extension = {
            ".geojson": "GeoJSON",
            ".json": "GeoJSON",
            ".gpkg": "GPKG",
            ".shp": "ESRI Shapefile",
        }
        suffix = path.suffix.lower()
        if suffix not in drivers_by_extension:
            raise ValueError("Use an output path ending in .geojson, .json, .gpkg, or .shp.")
        driver = drivers_by_extension[suffix]

    gdf.to_file(path, driver=driver, **kwargs)

    return path
