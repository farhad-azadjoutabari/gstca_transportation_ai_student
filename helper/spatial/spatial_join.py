"""Join two GeoDataFrames by location."""


def spatial_join(left_gdf, right_gdf, predicate="intersects", how="left"):
    """Join two spatial datasets using their geometry.

    A spatial join attaches columns from one dataset to another based on where
    features are located. For example, students can attach a census tract name
    to each traffic signal, or find which district each crash point is inside.

    Parameters
    ----------
    left_gdf : geopandas.GeoDataFrame
        Dataset that keeps its geometry in the result.
    right_gdf : geopandas.GeoDataFrame
        Dataset whose columns are joined onto the left dataset.
    predicate : str, default "intersects"
        Spatial relationship to use. Common choices include "intersects",
        "within", "contains", and "touches".
    how : {"left", "right", "inner"}, default "left"
        Type of join to perform.

    Returns
    -------
    geopandas.GeoDataFrame
        Joined spatial dataset.

    Example
    -------
    >>> from helper.data_read import read_shp_file
    >>> from helper.spatial import spatial_join
    >>> signals = read_shp_file("data/signalized_intersections_city_of_dallas/Signalized_Intersections.shp")
    >>> school_zones = read_shp_file("data/school_zones_city_of_dallas/School_Zones.shp")
    >>> signals_with_zone = spatial_join(signals, school_zones, predicate="within")
    """
    try:
        import geopandas as gpd
    except ImportError as exc:
        raise ImportError(
            "geopandas is required for spatial helpers. Install it with: pip install geopandas"
        ) from exc

    if not isinstance(left_gdf, gpd.GeoDataFrame):
        raise TypeError("spatial_join expects left_gdf to be a geopandas GeoDataFrame.")
    if not isinstance(right_gdf, gpd.GeoDataFrame):
        raise TypeError("spatial_join expects right_gdf to be a geopandas GeoDataFrame.")

    if (left_gdf.crs is None) != (right_gdf.crs is None):
        raise ValueError("Both GeoDataFrames need CRS values, or both should have no CRS.")

    right = right_gdf
    if left_gdf.crs is not None and right.crs is not None and left_gdf.crs != right.crs:
        right = right.to_crs(left_gdf.crs)

    return gpd.sjoin(left_gdf, right, how=how, predicate=predicate)
