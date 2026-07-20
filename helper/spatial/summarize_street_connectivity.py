"""Summarize approximate street-network connectivity by polygon."""

from ._join_helpers import (
    geometry_area_in_square_meters,
    geometry_length_in_meters,
    prepare_measurement_crs,
    require_geodataframes,
    unique_temp_column,
    unit_to_meters,
    unit_to_square_meters,
)


def summarize_street_connectivity(
    polygon_gdf,
    road_gdf,
    road_length_column="road_miles",
    road_density_column="road_miles_per_sq_mile",
    segment_count_column="road_segment_count",
    node_count_column="street_node_count",
    intersection_count_column="street_intersection_count",
    dead_end_count_column="dead_end_count",
    intersection_density_column="intersections_per_sq_mile",
    links_per_node_column="links_per_node",
    average_segment_length_column="avg_segment_length",
    unit="miles",
    area_unit="square_miles",
    projected_epsg=None,
    coordinate_precision=1,
):
    """Create tract- or zone-level street connectivity indicators.

    This function uses road-line endpoints as an approximate network node
    layer. It works best when road lines are already split at intersections,
    as most routable street-network files are. It does not replace detailed
    network analysis, but it gives students practical variables for roadway
    density, intersection density, dead ends, and average segment length.

    Parameters
    ----------
    polygon_gdf : geopandas.GeoDataFrame
        Polygon dataset receiving the network indicators, such as tracts,
        neighborhoods, or zones.
    road_gdf : geopandas.GeoDataFrame
        Road or street line dataset.
    road_length_column : str, default "road_miles"
        Output column for total road length.
    road_density_column : str, default "road_miles_per_sq_mile"
        Output column for road length divided by polygon area.
    segment_count_column : str, default "road_segment_count"
        Output column for unique road segments touching each polygon.
    node_count_column : str, default "street_node_count"
        Output column for street endpoint nodes in each polygon.
    intersection_count_column : str, default "street_intersection_count"
        Output column for nodes with degree 3 or higher.
    dead_end_count_column : str, default "dead_end_count"
        Output column for nodes with degree 1.
    intersection_density_column : str, default "intersections_per_sq_mile"
        Output column for intersections divided by polygon area.
    links_per_node_column : str, default "links_per_node"
        Output column for road segments divided by street nodes.
    average_segment_length_column : str, default "avg_segment_length"
        Output column for total road length divided by road segment count.
    unit : {"meters", "kilometers", "feet", "miles"}, default "miles"
        Unit for road length and average segment length.
    area_unit : {"square_meters", "square_kilometers", "square_feet", "square_miles", "acres"}, default "square_miles"
        Unit used in density denominators.
    projected_epsg : int, optional
        EPSG code to use temporarily for length and area calculations.
    coordinate_precision : int, default 1
        Number of decimal places used to merge nearly identical endpoint
        coordinates after projection.

    Returns
    -------
    geopandas.GeoDataFrame
        A copy of `polygon_gdf` with street-connectivity indicators.

    Example
    -------
    >>> from helper.spatial import summarize_street_connectivity
    >>> tracts = summarize_street_connectivity(
    ...     tracts,
    ...     local_roads,
    ...     projected_epsg=2276,
    ... )
    """
    gpd = require_geodataframes(
        "summarize_street_connectivity",
        polygon_gdf=polygon_gdf,
        road_gdf=road_gdf,
    )

    length_factor = unit_to_meters(unit)
    area_factor = unit_to_square_meters(area_unit)
    all_columns = set(polygon_gdf.columns) | set(road_gdf.columns)
    polygon_id = unique_temp_column(all_columns, "__polygon_join_id__")
    road_id = unique_temp_column(all_columns | {polygon_id}, "__road_join_id__")

    polygons = polygon_gdf.copy()
    roads = road_gdf.copy()
    polygons[polygon_id] = range(len(polygons))
    roads[road_id] = range(len(roads))

    measurement_polygons, measurement_roads = prepare_measurement_crs(
        polygons,
        roads,
        projected_epsg,
        "Street connectivity",
    )

    result = polygon_gdf.copy()
    result[polygon_id] = range(len(result))
    output_columns = [
        road_length_column,
        road_density_column,
        segment_count_column,
        node_count_column,
        intersection_count_column,
        dead_end_count_column,
        intersection_density_column,
        links_per_node_column,
        average_segment_length_column,
    ]
    for column in output_columns:
        if column is not None:
            result[column] = 0.0

    if measurement_polygons.empty or measurement_roads.empty:
        return result.drop(columns=polygon_id)

    polygon_geometry = measurement_polygons.geometry.name
    road_geometry = measurement_roads.geometry.name

    intersections = gpd.overlay(
        measurement_polygons[[polygon_id, polygon_geometry]],
        measurement_roads[[road_id, road_geometry]],
        how="intersection",
        keep_geom_type=False,
    )

    if not intersections.empty:
        raw_length_column = unique_temp_column(intersections.columns, "__raw_road_length__")
        intersections[raw_length_column] = geometry_length_in_meters(intersections)
        intersections = intersections[intersections[raw_length_column] > 0].copy()

    if not intersections.empty:
        length_summary = intersections.groupby(polygon_id)[raw_length_column].sum() / length_factor
        segment_summary = intersections.groupby(polygon_id)[road_id].nunique()
        result[road_length_column] = result[polygon_id].map(length_summary).fillna(0)
        result[segment_count_column] = (
            result[polygon_id].map(segment_summary).fillna(0).astype(int)
        )

    node_gdf = _build_road_endpoint_nodes(measurement_roads, road_id, coordinate_precision, gpd)
    if not node_gdf.empty:
        joined_nodes = gpd.sjoin(
            node_gdf,
            measurement_polygons[[polygon_id, polygon_geometry]],
            how="inner",
            predicate="intersects",
        )

        if not joined_nodes.empty:
            node_summary = joined_nodes.groupby(polygon_id).size()
            intersection_summary = (
                joined_nodes[joined_nodes["node_degree"] >= 3].groupby(polygon_id).size()
            )
            dead_end_summary = (
                joined_nodes[joined_nodes["node_degree"] == 1].groupby(polygon_id).size()
            )
            result[node_count_column] = result[polygon_id].map(node_summary).fillna(0).astype(int)
            result[intersection_count_column] = (
                result[polygon_id].map(intersection_summary).fillna(0).astype(int)
            )
            result[dead_end_count_column] = (
                result[polygon_id].map(dead_end_summary).fillna(0).astype(int)
            )

    area_summary = geometry_area_in_square_meters(measurement_polygons) / area_factor
    area_summary = area_summary.groupby(measurement_polygons[polygon_id]).first()

    if road_density_column is not None:
        result[road_density_column] = _safe_divide(
            result[road_length_column],
            result[polygon_id].map(area_summary),
        )
    if intersection_density_column is not None:
        result[intersection_density_column] = _safe_divide(
            result[intersection_count_column],
            result[polygon_id].map(area_summary),
        )
    if links_per_node_column is not None:
        result[links_per_node_column] = _safe_divide(
            result[segment_count_column],
            result[node_count_column],
        )
    if average_segment_length_column is not None:
        result[average_segment_length_column] = _safe_divide(
            result[road_length_column],
            result[segment_count_column],
        )

    integer_columns = [
        segment_count_column,
        node_count_column,
        intersection_count_column,
        dead_end_count_column,
    ]
    for column in integer_columns:
        if column is not None:
            result[column] = result[column].fillna(0).astype(int)

    return result.drop(columns=polygon_id)


def _build_road_endpoint_nodes(roads, road_id, coordinate_precision, gpd):
    """Build an approximate node layer from line endpoints."""
    import pandas as pd
    from shapely.geometry import Point

    records = []
    geometry_column = roads.geometry.name
    for _, road in roads[[road_id, geometry_column]].iterrows():
        current_road_id = road[road_id]
        geometry = road[geometry_column]
        for part in _iter_line_parts(geometry):
            coordinates = list(part.coords)
            if len(coordinates) < 2:
                continue

            for coordinate in (coordinates[0], coordinates[-1]):
                x_value = round(coordinate[0], coordinate_precision)
                y_value = round(coordinate[1], coordinate_precision)
                records.append(
                    {
                        "node_key": (x_value, y_value),
                        "road_id": current_road_id,
                        "geometry": Point(coordinate[0], coordinate[1]),
                    }
                )

    if not records:
        return gpd.GeoDataFrame(columns=["node_degree", "geometry"], geometry="geometry", crs=roads.crs)

    endpoint_df = pd.DataFrame(records)
    grouped = (
        endpoint_df.groupby("node_key")
        .agg(
            node_degree=("road_id", "nunique"),
            geometry=("geometry", "first"),
        )
        .reset_index(drop=True)
    )
    return gpd.GeoDataFrame(grouped, geometry="geometry", crs=roads.crs)


def _iter_line_parts(geometry):
    """Yield line parts from LineString, MultiLineString, or geometry collections."""
    if geometry is None or geometry.is_empty:
        return

    if geometry.geom_type == "LineString":
        yield geometry
    elif geometry.geom_type == "MultiLineString":
        yield from geometry.geoms
    elif geometry.geom_type == "GeometryCollection":
        for part in geometry.geoms:
            yield from _iter_line_parts(part)


def _safe_divide(numerator, denominator):
    """Divide while returning zero for missing or zero denominators."""
    result = numerator / denominator.replace(0, float("nan"))
    return result.fillna(0)
