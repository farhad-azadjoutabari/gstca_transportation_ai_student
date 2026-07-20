"""Summarize line features within a distance of each source feature."""

from ._access_helpers import set_analysis_geometry
from ._join_helpers import (
    geometry_length_in_meters,
    prepare_measurement_crs,
    require_geodataframes,
    unique_temp_column,
    unit_to_meters,
)


def summarize_lines_within_distance(
    source_gdf,
    line_gdf,
    distance,
    length_column="nearby_line_length",
    count_column="nearby_line_count",
    unit="meters",
    projected_epsg=None,
    source_geometry="geometry",
):
    """Measure nearby line length around each source feature.

    Use this for variables such as miles of major roads near a tract, bikeway
    miles near an intersection, bus-route miles near a neighborhood, or freight
    corridor length near a roadway segment.

    Parameters
    ----------
    source_gdf : geopandas.GeoDataFrame
        Features receiving the summary columns.
    line_gdf : geopandas.GeoDataFrame
        Line features to summarize, such as roads, bus routes, bikeways,
        trails, freight corridors, or speed/volume links.
    distance : float
        Buffer distance in the units of the projected CRS.
    length_column : str, default "nearby_line_length"
        Name of the output line-length column.
    count_column : str or None, default "nearby_line_count"
        Name of the output unique-line-count column. Set to None to skip it.
    unit : {"meters", "kilometers", "feet", "miles"}, default "meters"
        Unit for the output length column.
    projected_epsg : int, optional
        EPSG code to use temporarily for buffering and length calculations.
    source_geometry : {"geometry", "centroid", "representative_point"}, default "geometry"
        Geometry used as the source before buffering.

    Returns
    -------
    geopandas.GeoDataFrame
        A copy of `source_gdf` with nearby line length and optional count.

    Example
    -------
    >>> from helper.spatial import summarize_lines_within_distance
    >>> intersections = summarize_lines_within_distance(
    ...     intersections,
    ...     bikeways,
    ...     distance=1320,
    ...     length_column="bikeway_miles_within_quarter_mile",
    ...     unit="miles",
    ...     projected_epsg=2276,
    ... )
    """
    if distance < 0:
        raise ValueError("distance must be greater than or equal to zero.")

    gpd = require_geodataframes(
        "summarize_lines_within_distance",
        source_gdf=source_gdf,
        line_gdf=line_gdf,
    )
    meter_factor = unit_to_meters(unit)

    all_columns = set(source_gdf.columns) | set(line_gdf.columns)
    source_id = unique_temp_column(all_columns, "__source_join_id__")
    line_id = unique_temp_column(all_columns | {source_id}, "__line_join_id__")

    sources = source_gdf.copy()
    lines = line_gdf.copy()
    sources[source_id] = range(len(sources))
    lines[line_id] = range(len(lines))

    measurement_sources, measurement_lines = prepare_measurement_crs(
        sources,
        lines,
        projected_epsg,
        "Nearby line summary",
    )
    measurement_sources = set_analysis_geometry(
        measurement_sources,
        source_geometry,
        "summarize_lines_within_distance",
    )

    result = source_gdf.copy()
    result[source_id] = range(len(result))
    result[length_column] = 0.0
    if count_column is not None:
        result[count_column] = 0

    if measurement_sources.empty or measurement_lines.empty:
        return result.drop(columns=source_id)

    source_geometry_column = measurement_sources.geometry.name
    line_geometry_column = measurement_lines.geometry.name
    buffers = measurement_sources[[source_id, source_geometry_column]].copy()
    buffers[source_geometry_column] = measurement_sources.geometry.buffer(distance)

    intersections = gpd.overlay(
        buffers[[source_id, source_geometry_column]],
        measurement_lines[[line_id, line_geometry_column]],
        how="intersection",
        keep_geom_type=False,
    )

    if intersections.empty:
        return result.drop(columns=source_id)

    raw_length_column = unique_temp_column(intersections.columns, "__raw_overlap_length__")
    intersections[raw_length_column] = geometry_length_in_meters(intersections)
    intersections = intersections[intersections[raw_length_column] > 0].copy()

    if intersections.empty:
        return result.drop(columns=source_id)

    length_summary = intersections.groupby(source_id)[raw_length_column].sum() / meter_factor
    result[length_column] = result[source_id].map(length_summary).fillna(0)

    if count_column is not None:
        count_summary = intersections.groupby(source_id)[line_id].nunique()
        result[count_column] = result[source_id].map(count_summary).fillna(0).astype(int)

    return result.drop(columns=source_id)
