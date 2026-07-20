"""Summarize line lengths inside polygon features."""

from ._join_helpers import (
    geometry_length_in_meters,
    prepare_measurement_crs,
    require_geodataframes,
    unique_temp_column,
    unit_to_meters,
)


def summarize_lines_by_polygon(
    polygon_gdf,
    line_gdf,
    length_column="line_length",
    count_column="line_count",
    unit="meters",
    projected_epsg=None,
):
    """Calculate total line length inside each polygon.

    Use this when students need polygon-level totals from line layers. For
    example, this can calculate miles of trails, roads, bikeways, or bus routes
    inside each Census tract.

    Parameters
    ----------
    polygon_gdf : geopandas.GeoDataFrame
        Polygon dataset that receives the summary columns, such as Census
        tracts, neighborhoods, or zones.
    line_gdf : geopandas.GeoDataFrame
        Line dataset to summarize, such as roads, trails, routes, or links.
    length_column : str, default "line_length"
        Name of the output column containing total line length in each polygon.
    count_column : str or None, default "line_count"
        Name of the output column containing the number of input line features
        that overlap each polygon. Set to None to skip this column.
    unit : {"meters", "kilometers", "feet", "miles"}, default "meters"
        Unit for the output length column.
    projected_epsg : int, optional
        EPSG code to use temporarily for length calculations. Required when
        the input data is in longitude/latitude.

    Returns
    -------
    geopandas.GeoDataFrame
        A copy of `polygon_gdf` with total line length and optional line count
        columns added. Polygons with no matching lines receive zero values.

    Example
    -------
    >>> from helper.data_read import read_shp_file, read_geojson_file
    >>> from helper.spatial import summarize_lines_by_polygon
    >>> tracts = read_shp_file("path/to/census_tracts.shp")
    >>> bikeways = read_geojson_file("data/bikeway_dallas_county/bikeway_onstreet_existing.geojson")
    >>> tracts = summarize_lines_by_polygon(
    ...     tracts,
    ...     bikeways,
    ...     length_column="bikeway_miles",
    ...     unit="miles",
    ...     projected_epsg=2276,
    ... )
    """
    gpd = require_geodataframes(
        "summarize_lines_by_polygon",
        polygon_gdf=polygon_gdf,
        line_gdf=line_gdf,
    )

    meter_factor = unit_to_meters(unit)
    all_columns = set(polygon_gdf.columns) | set(line_gdf.columns)
    polygon_id = unique_temp_column(all_columns, "__polygon_join_id__")
    line_id = unique_temp_column(all_columns | {polygon_id}, "__line_join_id__")

    polygons = polygon_gdf.copy()
    lines = line_gdf.copy()
    polygons[polygon_id] = range(len(polygons))
    lines[line_id] = range(len(lines))

    measurement_polygons, measurement_lines = prepare_measurement_crs(
        polygons,
        lines,
        projected_epsg,
        "Line overlap length",
    )

    polygon_geometry = measurement_polygons.geometry.name
    line_geometry = measurement_lines.geometry.name
    intersections = gpd.overlay(
        measurement_polygons[[polygon_id, polygon_geometry]],
        measurement_lines[[line_id, line_geometry]],
        how="intersection",
        keep_geom_type=False,
    )

    result = polygon_gdf.copy()
    result[polygon_id] = range(len(result))

    if intersections.empty:
        result[length_column] = 0.0
        if count_column is not None:
            result[count_column] = 0
        return result.drop(columns=polygon_id)

    raw_length_column = unique_temp_column(intersections.columns, "__raw_overlap_length__")
    intersections[raw_length_column] = geometry_length_in_meters(intersections)
    intersections = intersections[intersections[raw_length_column] > 0].copy()

    if intersections.empty:
        result[length_column] = 0.0
        if count_column is not None:
            result[count_column] = 0
        return result.drop(columns=polygon_id)

    length_summary = intersections.groupby(polygon_id)[raw_length_column].sum() / meter_factor
    result[length_column] = result[polygon_id].map(length_summary).fillna(0)

    if count_column is not None:
        count_summary = intersections.groupby(polygon_id)[line_id].nunique()
        result[count_column] = result[polygon_id].map(count_summary).fillna(0).astype(int)

    return result.drop(columns=polygon_id)
