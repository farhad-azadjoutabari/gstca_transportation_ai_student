"""Summarize point features inside polygon features."""

from ._join_helpers import align_crs, require_geodataframes, unique_temp_column


def summarize_points_by_polygon(
    polygon_gdf,
    point_gdf,
    count_column="point_count",
    sum_columns=None,
    predicate="within",
):
    """Count points and sum point attributes inside each polygon.

    Use this when students need tract-level summaries from point layers. For
    example, this can count bus stops in each Census tract, count development
    projects in each tract, or sum employer jobs inside each tract.

    Parameters
    ----------
    polygon_gdf : geopandas.GeoDataFrame
        Polygon dataset that receives the summary columns, such as Census
        tracts, neighborhoods, or zones.
    point_gdf : geopandas.GeoDataFrame
        Point dataset to summarize, such as bus stops, employers, crashes, or
        development projects.
    count_column : str or None, default "point_count"
        Name of the output count column. Set to None if only sums are needed.
    sum_columns : str, list, dict, or None, default None
        Point attribute columns to sum inside each polygon. A string or list
        creates output columns named with a "sum_" prefix. A dictionary maps
        input column names to output column names, such as
        {"EMPLOYEES": "total_employees"}.
    predicate : str, default "within"
        Spatial relationship used to match points to polygons. Use "within"
        for points strictly inside polygons, or "intersects" if points on
        polygon boundaries should also be counted.

    Returns
    -------
    geopandas.GeoDataFrame
        A copy of `polygon_gdf` with point count and/or sum columns added.
        Polygons with no matching points receive zero values.

    Example
    -------
    >>> from helper.data_read import read_shp_file, read_gpkg_file
    >>> from helper.spatial import summarize_points_by_polygon
    >>> tracts = read_shp_file("path/to/census_tracts.shp")
    >>> bus_stops = read_shp_file("data/dallas_dart_bus/Dallas-DART-Stops/Bus_Stops.shp")
    >>> tracts = summarize_points_by_polygon(tracts, bus_stops, count_column="bus_stop_count")
    >>> employers = read_gpkg_file("data/employers_dallas_county/DallasCounty-Employer.gpkg")
    >>> tracts = summarize_points_by_polygon(
    ...     tracts,
    ...     employers,
    ...     count_column="employer_count",
    ...     sum_columns={"EMPLOYEES": "total_employees"},
    ... )
    """
    gpd = require_geodataframes(
        "summarize_points_by_polygon",
        polygon_gdf=polygon_gdf,
        point_gdf=point_gdf,
    )

    if sum_columns is None:
        sum_mapping = {}
    elif isinstance(sum_columns, str):
        sum_mapping = {sum_columns: f"sum_{sum_columns}"}
    elif isinstance(sum_columns, dict):
        sum_mapping = dict(sum_columns)
    else:
        sum_mapping = {column: f"sum_{column}" for column in sum_columns}

    missing = [column for column in sum_mapping if column not in point_gdf.columns]
    if missing:
        raise ValueError(f"sum_columns contains columns that were not found: {missing}")

    points = align_crs(polygon_gdf, point_gdf)

    polygon_id = unique_temp_column(polygon_gdf.columns, "__polygon_join_id__")
    polygons = polygon_gdf.copy()
    polygons[polygon_id] = range(len(polygons))

    polygon_geometry = polygons.geometry.name
    joined = gpd.sjoin(
        points,
        polygons[[polygon_id, polygon_geometry]],
        how="inner",
        predicate=predicate,
    )

    result = polygon_gdf.copy()
    result[polygon_id] = range(len(result))

    if count_column is not None:
        counts = joined.groupby(polygon_id).size()
        result[count_column] = result[polygon_id].map(counts).fillna(0).astype(int)

    if sum_mapping:
        import pandas as pd

        for source_column, output_column in sum_mapping.items():
            values = pd.to_numeric(joined[source_column], errors="coerce")
            sums = values.groupby(joined[polygon_id]).sum()
            result[output_column] = result[polygon_id].map(sums).fillna(0)

    return result.drop(columns=polygon_id)
