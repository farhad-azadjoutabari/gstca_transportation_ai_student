"""Summarize crash points by polygon area."""

from ._safety_helpers import check_columns, require_geopandas


def summarize_crashes_by_area(
    crash_gdf,
    area_gdf,
    count_column="crash_count",
    severity_column=None,
    predicate="within",
):
    """Count crash points inside each polygon area.

    Use this to create tract-level or zone-level crash summaries for Challenge
    3. If a severity column is provided, the output also includes crash counts
    by severity category.

    Parameters
    ----------
    crash_gdf : geopandas.GeoDataFrame
        Crash point layer.
    area_gdf : geopandas.GeoDataFrame
        Polygon layer, such as Census tracts or zones.
    count_column : str, default "crash_count"
        Name of the total crash count column.
    severity_column : str, optional
        Crash severity column used to create category counts.
    predicate : str, default "within"
        Spatial relationship used to match crashes to polygons.

    Returns
    -------
    geopandas.GeoDataFrame
        Copy of `area_gdf` with crash count columns added.

    Example
    -------
    >>> from helper.safety import summarize_crashes_by_area
    >>> tracts = summarize_crashes_by_area(crashes, tracts, severity_column="severity")
    """
    gpd = require_geopandas("summarize_crashes_by_area")
    if not isinstance(crash_gdf, gpd.GeoDataFrame) or not isinstance(area_gdf, gpd.GeoDataFrame):
        raise TypeError("summarize_crashes_by_area expects GeoDataFrames.")
    if severity_column is not None:
        check_columns(crash_gdf, [severity_column], "severity_column")

    from helper.spatial import summarize_points_by_polygon

    result = summarize_points_by_polygon(
        area_gdf,
        crash_gdf,
        count_column=count_column,
        predicate=predicate,
    )

    if severity_column is None:
        return result

    areas = area_gdf.copy()
    area_id = "_area_crash_join_id"
    while area_id in areas.columns:
        area_id = f"_{area_id}"
    areas[area_id] = range(len(areas))
    area_geometry = areas.geometry.name
    crashes = crash_gdf.to_crs(areas.crs) if crash_gdf.crs != areas.crs else crash_gdf
    joined = gpd.sjoin(
        crashes[[severity_column, crashes.geometry.name]],
        areas[[area_id, area_geometry]],
        how="inner",
        predicate=predicate,
    )
    if joined.empty:
        return result

    severity_counts = (
        joined.groupby([area_id, severity_column]).size().unstack(fill_value=0).add_prefix("crash_")
    )
    result[area_id] = range(len(result))
    result = result.join(severity_counts, on=area_id)
    for column in severity_counts.columns:
        result[column] = result[column].fillna(0).astype(int)
    return result.drop(columns=area_id)
