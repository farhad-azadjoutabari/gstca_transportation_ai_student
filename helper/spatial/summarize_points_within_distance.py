"""Summarize point features within a distance of each source feature."""

from ._access_helpers import normalize_sum_columns, set_analysis_geometry
from ._join_helpers import prepare_measurement_crs, require_geodataframes, unique_temp_column


def summarize_points_within_distance(
    source_gdf,
    point_gdf,
    distance,
    count_column="nearby_point_count",
    sum_columns=None,
    projected_epsg=None,
    source_geometry="geometry",
    predicate="intersects",
):
    """Count and sum nearby point features around each source feature.

    Use this for accessibility and context measures such as jobs within three
    miles of each tract centroid, bus stops within a half mile of each tract,
    crashes near each road segment, or signals near each intersection.

    Parameters
    ----------
    source_gdf : geopandas.GeoDataFrame
        Features receiving the summary columns, such as tracts, intersections,
        roads, or zones.
    point_gdf : geopandas.GeoDataFrame
        Point features to summarize, such as employers, bus stops, crashes,
        traffic signals, schools, medical facilities, or retail destinations.
    distance : float
        Buffer distance in the units of the projected CRS. For EPSG:2276 this
        is feet, so a half mile is 2640.
    count_column : str or None, default "nearby_point_count"
        Name of the output point-count column. Set to None to skip counts.
    sum_columns : str, list, dict, or None, default None
        Point attribute columns to sum inside each buffer. A string or list
        creates output columns named with a "sum_" prefix. A dictionary maps
        input column names to output names, such as {"EMPLOYEES": "nearby_jobs"}.
    projected_epsg : int, optional
        EPSG code to use temporarily for buffering and distance calculations.
    source_geometry : {"geometry", "centroid", "representative_point"}, default "geometry"
        Geometry used as the source before buffering. Use "centroid" for
        tract-center accessibility measures.
    predicate : str, default "intersects"
        Spatial predicate used to match points to buffers.

    Returns
    -------
    geopandas.GeoDataFrame
        A copy of `source_gdf` with nearby point count and/or sum columns.

    Example
    -------
    >>> from helper.spatial import summarize_points_within_distance
    >>> tracts = summarize_points_within_distance(
    ...     tracts,
    ...     employers,
    ...     distance=5280 * 3,
    ...     sum_columns={"EMPLOYEES": "jobs_within_3_miles"},
    ...     projected_epsg=2276,
    ...     source_geometry="centroid",
    ... )
    """
    if distance < 0:
        raise ValueError("distance must be greater than or equal to zero.")

    gpd = require_geodataframes(
        "summarize_points_within_distance",
        source_gdf=source_gdf,
        point_gdf=point_gdf,
    )
    sum_mapping = normalize_sum_columns(sum_columns, point_gdf.columns)

    all_columns = set(source_gdf.columns) | set(point_gdf.columns)
    source_id = unique_temp_column(all_columns, "__source_join_id__")

    sources = source_gdf.copy()
    points = point_gdf.copy()
    sources[source_id] = range(len(sources))

    measurement_sources, measurement_points = prepare_measurement_crs(
        sources,
        points,
        projected_epsg,
        "Nearby point summary",
    )
    measurement_sources = set_analysis_geometry(
        measurement_sources,
        source_geometry,
        "summarize_points_within_distance",
    )

    result = source_gdf.copy()
    result[source_id] = range(len(result))

    if count_column is not None:
        result[count_column] = 0
    for output_column in sum_mapping.values():
        result[output_column] = 0.0

    if measurement_sources.empty or measurement_points.empty:
        return result.drop(columns=source_id)

    geometry_column = measurement_sources.geometry.name
    buffers = measurement_sources[[source_id, geometry_column]].copy()
    buffers[geometry_column] = measurement_sources.geometry.buffer(distance)

    joined = gpd.sjoin(
        measurement_points,
        buffers[[source_id, geometry_column]],
        how="inner",
        predicate=predicate,
    )

    if joined.empty:
        return result.drop(columns=source_id)

    if count_column is not None:
        counts = joined.groupby(source_id).size()
        result[count_column] = result[source_id].map(counts).fillna(0).astype(int)

    if sum_mapping:
        import pandas as pd

        for source_column, output_column in sum_mapping.items():
            values = pd.to_numeric(joined[source_column], errors="coerce")
            sums = values.groupby(joined[source_id]).sum()
            result[output_column] = result[source_id].map(sums).fillna(0)

    return result.drop(columns=source_id)
