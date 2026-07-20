"""Summarize polygon overlap areas inside polygon features."""

from ._join_helpers import (
    geometry_area_in_square_meters,
    prepare_measurement_crs,
    require_geodataframes,
    safe_column_suffix,
    unique_temp_column,
    unit_to_square_meters,
)


def summarize_polygons_by_polygon(
    polygon_gdf,
    overlap_gdf,
    area_column="overlap_area",
    count_column="polygon_count",
    category_column=None,
    category_area_prefix=None,
    unit="square_meters",
    projected_epsg=None,
):
    """Calculate total overlapping polygon area inside each polygon.

    Use this when students need tract-level totals from polygon layers. For
    example, this can calculate acres of parks inside each tract, acres of
    on-demand transit zones inside each tract, or acres of each land-use type
    inside each tract.

    Parameters
    ----------
    polygon_gdf : geopandas.GeoDataFrame
        Polygon dataset that receives the summary columns, such as Census
        tracts, neighborhoods, or zones.
    overlap_gdf : geopandas.GeoDataFrame
        Polygon dataset to summarize inside `polygon_gdf`, such as parks,
        service areas, land-use polygons, or congestion polygons.
    area_column : str, default "overlap_area"
        Name of the output column containing total overlap area.
    count_column : str or None, default "polygon_count"
        Name of the output column containing the number of input polygon
        features that overlap each base polygon. Set to None to skip this
        column.
    category_column : str, optional
        Column in `overlap_gdf` used to create separate area columns by
        category, such as park type or land-use class.
    category_area_prefix : str, optional
        Prefix for category-specific area columns. By default, this is
        `area_column` followed by an underscore.
    unit : {"square_meters", "square_kilometers", "square_feet", "square_miles", "acres"}, default "square_meters"
        Unit for area output columns.
    projected_epsg : int, optional
        EPSG code to use temporarily for area calculations. Required when the
        input data is in longitude/latitude.

    Returns
    -------
    geopandas.GeoDataFrame
        A copy of `polygon_gdf` with total overlap area, optional overlap
        count, and optional category-specific area columns added. Polygons with
        no overlap receive zero values.

    Example
    -------
    >>> from helper.data_read import read_shp_file, read_gpkg_file
    >>> from helper.spatial import summarize_polygons_by_polygon
    >>> tracts = read_shp_file("path/to/census_tracts.shp")
    >>> parks = read_gpkg_file("data/parks_dallas_county/DallasCounty-Parks.gpkg")
    >>> tracts = summarize_polygons_by_polygon(
    ...     tracts,
    ...     parks,
    ...     area_column="park_acres",
    ...     unit="acres",
    ...     projected_epsg=2276,
    ... )
    """
    gpd = require_geodataframes(
        "summarize_polygons_by_polygon",
        polygon_gdf=polygon_gdf,
        overlap_gdf=overlap_gdf,
    )

    if category_column is not None and category_column not in overlap_gdf.columns:
        raise ValueError(f"category_column was not found: {category_column}")

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

    polygon_geometry = measurement_polygons.geometry.name
    overlap_geometry = measurement_overlaps.geometry.name
    overlap_columns = [overlap_id, overlap_geometry]
    if category_column is not None:
        overlap_columns.insert(1, category_column)

    intersections = gpd.overlay(
        measurement_polygons[[polygon_id, polygon_geometry]],
        measurement_overlaps[overlap_columns],
        how="intersection",
        keep_geom_type=True,
    )

    result = polygon_gdf.copy()
    result[polygon_id] = range(len(result))

    if intersections.empty:
        result[area_column] = 0.0
        if count_column is not None:
            result[count_column] = 0
        return result.drop(columns=polygon_id)

    raw_area_column = unique_temp_column(intersections.columns, "__raw_overlap_area__")
    intersections[raw_area_column] = geometry_area_in_square_meters(intersections)
    intersections = intersections[intersections[raw_area_column] > 0].copy()

    if intersections.empty:
        result[area_column] = 0.0
        if count_column is not None:
            result[count_column] = 0
        return result.drop(columns=polygon_id)

    area_summary = intersections.groupby(polygon_id)[raw_area_column].sum() / square_meter_factor
    result[area_column] = result[polygon_id].map(area_summary).fillna(0)

    if count_column is not None:
        count_summary = intersections.groupby(polygon_id)[overlap_id].nunique()
        result[count_column] = result[polygon_id].map(count_summary).fillna(0).astype(int)

    if category_column is not None:
        category_prefix = category_area_prefix
        if category_prefix is None:
            category_prefix = f"{area_column}_"

        category_values = intersections[category_column].fillna("missing")
        category_summary = (
            intersections.assign(__category_value__=category_values)
            .groupby([polygon_id, "__category_value__"])[raw_area_column]
            .sum()
            .unstack(fill_value=0)
            / square_meter_factor
        )

        used_columns = set(result.columns)
        category_output_names = {}
        for category_value in category_summary.columns:
            output_name = f"{category_prefix}{safe_column_suffix(category_value)}"
            if output_name in used_columns:
                output_name = f"{output_name}_category"

            base_output_name = output_name
            counter = 2
            while output_name in used_columns:
                output_name = f"{base_output_name}_{counter}"
                counter += 1

            category_output_names[category_value] = output_name
            used_columns.add(output_name)

        for category_value, output_name in category_output_names.items():
            result[output_name] = (
                result[polygon_id].map(category_summary[category_value]).fillna(0)
            )

    return result.drop(columns=polygon_id)
