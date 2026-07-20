"""Summarize crashes near intersections."""

from ._safety_helpers import check_columns, require_geopandas, unique_temp_column


def summarize_crashes_by_intersection(
    crash_gdf,
    intersection_gdf,
    buffer_distance,
    count_column="crash_count",
    intersection_id_column=None,
    projected_epsg=None,
):
    """Count crashes within a buffer of each intersection.

    Use this for Challenge 4 when students need crash occurrence at or near
    intersections. The function buffers each intersection point, counts nearby
    crashes, and returns the original intersection geometries.

    Parameters
    ----------
    crash_gdf : geopandas.GeoDataFrame
        Crash point layer.
    intersection_gdf : geopandas.GeoDataFrame
        Intersection point layer.
    buffer_distance : float
        Buffer distance in the units of the projected CRS.
    count_column : str, default "crash_count"
        Name of the output crash count column.
    intersection_id_column : str, optional
        Existing intersection ID column. If None, a temporary row ID is used.
    projected_epsg : int, optional
        EPSG code used temporarily for buffering.

    Returns
    -------
    geopandas.GeoDataFrame
        Copy of `intersection_gdf` with nearby crash counts added.

    Example
    -------
    >>> from helper.safety import summarize_crashes_by_intersection
    >>> intersections = summarize_crashes_by_intersection(crashes, intersections, buffer_distance=150, projected_epsg=2276)
    """
    gpd = require_geopandas("summarize_crashes_by_intersection")
    if not isinstance(crash_gdf, gpd.GeoDataFrame) or not isinstance(intersection_gdf, gpd.GeoDataFrame):
        raise TypeError("summarize_crashes_by_intersection expects GeoDataFrames.")
    if intersection_id_column is not None:
        check_columns(intersection_gdf, [intersection_id_column], "intersection_id_column")

    from helper.spatial import buffer_features, summarize_points_by_polygon

    intersection_id = intersection_id_column or unique_temp_column(
        intersection_gdf.columns,
        "_intersection_join_id",
    )
    intersections = intersection_gdf.copy()
    if intersection_id_column is None:
        intersections[intersection_id] = range(len(intersections))

    buffers = buffer_features(intersections, buffer_distance, projected_epsg=projected_epsg)
    buffer_counts = summarize_points_by_polygon(
        buffers[[intersection_id, buffers.geometry.name]],
        crash_gdf,
        count_column=count_column,
    )

    result = intersections.merge(buffer_counts[[intersection_id, count_column]], on=intersection_id, how="left")
    result[count_column] = result[count_column].fillna(0).astype(int)
    if intersection_id_column is None:
        result = result.drop(columns=intersection_id)
    return result
