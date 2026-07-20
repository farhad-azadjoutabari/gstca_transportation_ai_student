"""Assign line features to polygons by maximum length overlap."""

from ._join_helpers import (
    geometry_length_in_meters,
    list_columns,
    output_column_names,
    prepare_measurement_crs,
    require_geodataframes,
    unique_temp_column,
    unit_to_meters,
)


def assign_lines_by_max_overlap(
    line_gdf,
    polygon_gdf,
    polygon_columns=None,
    overlap_length_column="overlap_length",
    overlap_fraction_column="overlap_fraction",
    unit="meters",
    projected_epsg=None,
    polygon_prefix="",
):
    """Label each line with the polygon where most of the line falls.

    Use this when a line can cross more than one tract but should receive one
    tract label. For example, if 80 percent of a road link is in one Census
    tract and 20 percent is in another, this function assigns the link to the
    tract containing the longest part of the link.

    Parameters
    ----------
    line_gdf : geopandas.GeoDataFrame
        Line dataset to label, such as roadway links, bus routes, trails, or
        freight network segments.
    polygon_gdf : geopandas.GeoDataFrame
        Polygon dataset used for labels, such as Census tracts or districts.
    polygon_columns : str, list, or None, default None
        Columns from `polygon_gdf` to attach to each line. By default, all
        non-geometry polygon columns are attached.
    overlap_length_column : str, default "overlap_length"
        Name of the output column containing the winning overlap length.
    overlap_fraction_column : str or None, default "overlap_fraction"
        Name of the output column containing the share of the line inside the
        winning polygon. Set to None to skip this column.
    unit : {"meters", "kilometers", "feet", "miles"}, default "meters"
        Unit for the overlap length column.
    projected_epsg : int, optional
        EPSG code to use temporarily for length calculations. Required when
        the input data is in longitude/latitude.
    polygon_prefix : str, default ""
        Optional prefix added to attached polygon columns.

    Returns
    -------
    geopandas.GeoDataFrame
        A copy of `line_gdf` with selected polygon columns, winning overlap
        length, and winning overlap fraction added. Lines with no polygon
        overlap keep their geometry and receive missing polygon values.

    Example
    -------
    >>> from helper.data_read import read_shp_file
    >>> from helper.spatial import assign_lines_by_max_overlap
    >>> links = read_shp_file("data/speed_limits_city_of_dallas/Speed_Limits.shp")
    >>> tracts = read_shp_file("path/to/census_tracts.shp")
    >>> links_with_tract = assign_lines_by_max_overlap(
    ...     links,
    ...     tracts,
    ...     polygon_columns=["GEOID"],
    ...     projected_epsg=2276,
    ... )
    """
    gpd = require_geodataframes(
        "assign_lines_by_max_overlap",
        line_gdf=line_gdf,
        polygon_gdf=polygon_gdf,
    )

    meter_factor = unit_to_meters(unit)
    all_columns = set(line_gdf.columns) | set(polygon_gdf.columns)
    line_id = unique_temp_column(all_columns, "__line_join_id__")
    polygon_id = unique_temp_column(all_columns | {line_id}, "__polygon_join_id__")

    lines = line_gdf.copy()
    polygons = polygon_gdf.copy()
    lines[line_id] = range(len(lines))
    polygons[polygon_id] = range(len(polygons))

    measurement_lines, measurement_polygons = prepare_measurement_crs(
        lines,
        polygons,
        projected_epsg,
        "Line overlap length",
    )

    line_lengths = geometry_length_in_meters(measurement_lines).groupby(measurement_lines[line_id]).first()
    line_geometry = measurement_lines.geometry.name
    polygon_geometry = measurement_polygons.geometry.name

    intersections = gpd.overlay(
        measurement_lines[[line_id, line_geometry]],
        measurement_polygons[[polygon_id, polygon_geometry]],
        how="intersection",
        keep_geom_type=True,
    )

    polygon_available_columns = [
        column for column in polygon_gdf.columns if column != polygon_gdf.geometry.name
    ]
    selected_columns = list_columns(
        polygon_columns,
        polygon_available_columns,
        "polygon_columns",
    )
    rename_columns = output_column_names(
        selected_columns,
        list(line_gdf.columns) + [overlap_length_column, overlap_fraction_column],
        prefix=polygon_prefix,
        collision_suffix="_polygon",
    )
    polygon_attributes = polygons[[polygon_id] + selected_columns].rename(columns=rename_columns)

    import pandas as pd

    if intersections.empty:
        winners = pd.DataFrame(columns=[line_id, polygon_id])
    else:
        raw_overlap_column = unique_temp_column(intersections.columns, "__raw_overlap_length__")
        intersections[raw_overlap_column] = geometry_length_in_meters(intersections)
        intersections = intersections[intersections[raw_overlap_column] > 0].copy()

        if intersections.empty:
            winners = pd.DataFrame(columns=[line_id, polygon_id])
        else:
            intersections[overlap_length_column] = intersections[raw_overlap_column] / meter_factor

            if overlap_fraction_column is not None:
                total_lengths = intersections[line_id].map(line_lengths)
                intersections[overlap_fraction_column] = (
                    intersections[raw_overlap_column] / total_lengths
                ).fillna(0)

            winners = (
                intersections.sort_values(
                    [line_id, raw_overlap_column, polygon_id],
                    ascending=[True, False, True],
                )
                .drop_duplicates(line_id)
                .drop(columns=intersections.geometry.name)
            )

    output_columns = [line_id, polygon_id, overlap_length_column]
    if overlap_fraction_column is not None:
        output_columns.append(overlap_fraction_column)

    winners = winners[[column for column in output_columns if column in winners.columns]]
    winners = winners.merge(polygon_attributes, on=polygon_id, how="left").drop(columns=polygon_id)

    result = line_gdf.copy()
    result[line_id] = range(len(result))
    for column in [overlap_length_column, overlap_fraction_column]:
        if column is not None and column in result.columns:
            result = result.drop(columns=column)

    result = result.join(winners.set_index(line_id), on=line_id)
    if overlap_length_column not in result.columns:
        result[overlap_length_column] = 0
    result[overlap_length_column] = result[overlap_length_column].fillna(0)
    if overlap_fraction_column is not None:
        if overlap_fraction_column not in result.columns:
            result[overlap_fraction_column] = 0
        result[overlap_fraction_column] = result[overlap_fraction_column].fillna(0)

    return result.drop(columns=line_id)
