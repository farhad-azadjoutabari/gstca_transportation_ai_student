"""Assign polygons to other polygons by maximum area overlap."""

from ._join_helpers import (
    geometry_area_in_square_meters,
    list_columns,
    output_column_names,
    prepare_measurement_crs,
    require_geodataframes,
    unique_temp_column,
    unit_to_square_meters,
)


def assign_polygons_by_max_overlap(
    polygon_gdf,
    overlap_gdf,
    overlap_columns=None,
    overlap_area_column="overlap_area",
    overlap_fraction_column="overlap_fraction",
    unit="square_meters",
    projected_epsg=None,
    overlap_prefix="",
):
    """Label each polygon with the overlapping polygon that covers it most.

    Use this when a larger polygon layer needs to be assigned to tract-level
    polygons by dominant overlap. For example, if a tract overlaps severe
    congestion more than medium or uncongested areas, this function assigns
    the severe congestion value to that tract.

    Parameters
    ----------
    polygon_gdf : geopandas.GeoDataFrame
        Polygon dataset that receives the label, such as Census tracts.
    overlap_gdf : geopandas.GeoDataFrame
        Polygon dataset providing the label, such as congestion severity
        polygons, service areas, or transit-on-demand zones.
    overlap_columns : str, list, or None, default None
        Columns from `overlap_gdf` to attach to each polygon. By default, all
        non-geometry columns from `overlap_gdf` are attached.
    overlap_area_column : str, default "overlap_area"
        Name of the output column containing the winning overlap area.
    overlap_fraction_column : str or None, default "overlap_fraction"
        Name of the output column containing the share of each base polygon
        covered by the winning overlap polygon. Set to None to skip this
        column.
    unit : {"square_meters", "square_kilometers", "square_feet", "square_miles", "acres"}, default "square_meters"
        Unit for the overlap area column.
    projected_epsg : int, optional
        EPSG code to use temporarily for area calculations. Required when the
        input data is in longitude/latitude.
    overlap_prefix : str, default ""
        Optional prefix added to attached overlap polygon columns.

    Returns
    -------
    geopandas.GeoDataFrame
        A copy of `polygon_gdf` with selected columns from the dominant
        overlapping polygon, winning overlap area, and winning overlap
        fraction added.

    Example
    -------
    >>> from helper.data_read import read_shp_file
    >>> from helper.spatial import assign_polygons_by_max_overlap
    >>> tracts = read_shp_file("path/to/census_tracts.shp")
    >>> congestion = read_shp_file("data/dfw_mobility_level_of_congestion_2050/Mobility_2050_Level_of_Congestion_(2026).shp")
    >>> tracts_with_congestion = assign_polygons_by_max_overlap(
    ...     tracts,
    ...     congestion,
    ...     overlap_columns=["CONGESTION"],
    ...     projected_epsg=2276,
    ... )
    """
    gpd = require_geodataframes(
        "assign_polygons_by_max_overlap",
        polygon_gdf=polygon_gdf,
        overlap_gdf=overlap_gdf,
    )

    square_meter_factor = unit_to_square_meters(unit)
    all_columns = set(polygon_gdf.columns) | set(overlap_gdf.columns)
    polygon_id = unique_temp_column(all_columns, "__polygon_join_id__")
    overlap_id = unique_temp_column(all_columns | {polygon_id}, "__overlap_join_id__")

    polygons = polygon_gdf.copy()
    overlaps = overlap_gdf.copy()
    polygons[polygon_id] = range(len(polygons))
    overlaps[overlap_id] = range(len(overlaps))

    measurement_polygons, measurement_overlaps = prepare_measurement_crs(
        polygons,
        overlaps,
        projected_epsg,
        "Polygon overlap area",
    )

    polygon_areas = geometry_area_in_square_meters(measurement_polygons).groupby(
        measurement_polygons[polygon_id]
    ).first()
    polygon_geometry = measurement_polygons.geometry.name
    overlap_geometry = measurement_overlaps.geometry.name

    intersections = gpd.overlay(
        measurement_polygons[[polygon_id, polygon_geometry]],
        measurement_overlaps[[overlap_id, overlap_geometry]],
        how="intersection",
        keep_geom_type=True,
    )

    overlap_available_columns = [
        column for column in overlap_gdf.columns if column != overlap_gdf.geometry.name
    ]
    selected_columns = list_columns(
        overlap_columns,
        overlap_available_columns,
        "overlap_columns",
    )
    rename_columns = output_column_names(
        selected_columns,
        list(polygon_gdf.columns) + [overlap_area_column, overlap_fraction_column],
        prefix=overlap_prefix,
        collision_suffix="_overlap",
    )
    overlap_attributes = overlaps[[overlap_id] + selected_columns].rename(columns=rename_columns)

    import pandas as pd

    if intersections.empty:
        winners = pd.DataFrame(columns=[polygon_id, overlap_id])
    else:
        raw_overlap_column = unique_temp_column(intersections.columns, "__raw_overlap_area__")
        intersections[raw_overlap_column] = geometry_area_in_square_meters(intersections)
        intersections = intersections[intersections[raw_overlap_column] > 0].copy()

        if intersections.empty:
            winners = pd.DataFrame(columns=[polygon_id, overlap_id])
        else:
            intersections[overlap_area_column] = intersections[raw_overlap_column] / square_meter_factor

            if overlap_fraction_column is not None:
                total_areas = intersections[polygon_id].map(polygon_areas)
                intersections[overlap_fraction_column] = (
                    intersections[raw_overlap_column] / total_areas
                ).fillna(0)

            winners = (
                intersections.sort_values(
                    [polygon_id, raw_overlap_column, overlap_id],
                    ascending=[True, False, True],
                )
                .drop_duplicates(polygon_id)
                .drop(columns=intersections.geometry.name)
            )

    output_columns = [polygon_id, overlap_id, overlap_area_column]
    if overlap_fraction_column is not None:
        output_columns.append(overlap_fraction_column)

    winners = winners[[column for column in output_columns if column in winners.columns]]
    winners = winners.merge(overlap_attributes, on=overlap_id, how="left").drop(columns=overlap_id)

    result = polygon_gdf.copy()
    result[polygon_id] = range(len(result))
    for column in [overlap_area_column, overlap_fraction_column]:
        if column is not None and column in result.columns:
            result = result.drop(columns=column)

    result = result.join(winners.set_index(polygon_id), on=polygon_id)
    if overlap_area_column not in result.columns:
        result[overlap_area_column] = 0
    result[overlap_area_column] = result[overlap_area_column].fillna(0)
    if overlap_fraction_column is not None:
        if overlap_fraction_column not in result.columns:
            result[overlap_fraction_column] = 0
        result[overlap_fraction_column] = result[overlap_fraction_column].fillna(0)

    return result.drop(columns=polygon_id)
