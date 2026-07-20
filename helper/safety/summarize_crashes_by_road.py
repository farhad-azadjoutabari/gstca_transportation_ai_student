"""Summarize crashes near road segments."""

from ._safety_helpers import check_columns, require_geopandas, unique_temp_column


def summarize_crashes_by_road(
    crash_gdf,
    road_gdf,
    buffer_distance,
    count_column="crash_count",
    road_id_column=None,
    projected_epsg=None,
):
    """Count crashes within a buffer of each road segment.

    Use this for road safety analysis when crash points do not already have a
    road segment ID. The function buffers each road, counts nearby crashes,
    and returns the original road geometries with crash counts added.

    Parameters
    ----------
    crash_gdf : geopandas.GeoDataFrame
        Crash point layer.
    road_gdf : geopandas.GeoDataFrame
        Road or link line layer.
    buffer_distance : float
        Buffer distance in the units of the projected CRS.
    count_column : str, default "crash_count"
        Name of the output crash count column.
    road_id_column : str, optional
        Existing road ID column. If None, a temporary row ID is used.
    projected_epsg : int, optional
        EPSG code used temporarily for buffering.

    Returns
    -------
    geopandas.GeoDataFrame
        Copy of `road_gdf` with nearby crash counts added.

    Example
    -------
    >>> from helper.safety import summarize_crashes_by_road
    >>> roads = summarize_crashes_by_road(crashes, roads, buffer_distance=100, projected_epsg=2276)
    """
    gpd = require_geopandas("summarize_crashes_by_road")
    if not isinstance(crash_gdf, gpd.GeoDataFrame) or not isinstance(road_gdf, gpd.GeoDataFrame):
        raise TypeError("summarize_crashes_by_road expects GeoDataFrames.")
    if road_id_column is not None:
        check_columns(road_gdf, [road_id_column], "road_id_column")

    from helper.spatial import buffer_features, summarize_points_by_polygon

    road_id = road_id_column or unique_temp_column(road_gdf.columns, "_road_join_id")
    roads = road_gdf.copy()
    if road_id_column is None:
        roads[road_id] = range(len(roads))

    buffers = buffer_features(roads, buffer_distance, projected_epsg=projected_epsg)
    buffer_counts = summarize_points_by_polygon(buffers[[road_id, buffers.geometry.name]], crash_gdf, count_column=count_column)

    result = roads.merge(buffer_counts[[road_id, count_column]], on=road_id, how="left")
    result[count_column] = result[count_column].fillna(0).astype(int)
    if road_id_column is None:
        result = result.drop(columns=road_id)
    return result
