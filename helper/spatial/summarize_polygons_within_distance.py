"""Summarize polygon features within a distance of each source feature."""

from ._access_helpers import set_analysis_geometry
from ._join_helpers import (
    geometry_area_in_square_meters,
    prepare_measurement_crs,
    require_geodataframes,
    safe_column_suffix,
    unique_temp_column,
    unit_to_square_meters,
)


def summarize_polygons_within_distance(
    source_gdf,
    polygon_gdf,
    distance,
    area_column="nearby_polygon_area",
    count_column="nearby_polygon_count",
    category_column=None,
    category_area_prefix=None,
    unit="square_meters",
    projected_epsg=None,
    source_geometry="geometry",
):
    """Measure nearby polygon area around each source feature.

    Use this for land use, parks, service zones, airports, development areas,
    and other polygon context near tracts, roads, or intersections.

    Parameters
    ----------
    source_gdf : geopandas.GeoDataFrame
        Features receiving the summary columns.
    polygon_gdf : geopandas.GeoDataFrame
        Polygon features to summarize around each source.
    distance : float
        Buffer distance in the units of the projected CRS.
    area_column : str, default "nearby_polygon_area"
        Name of the output area column.
    count_column : str or None, default "nearby_polygon_count"
        Name of the output unique-polygon-count column. Set to None to skip it.
    category_column : str, optional
        Column in `polygon_gdf` used to create separate area columns by
        category, such as land-use type.
    category_area_prefix : str, optional
        Prefix for category-specific area columns.
    unit : {"square_meters", "square_kilometers", "square_feet", "square_miles", "acres"}, default "square_meters"
        Unit for area output columns.
    projected_epsg : int, optional
        EPSG code to use temporarily for buffering and area calculations.
    source_geometry : {"geometry", "centroid", "representative_point"}, default "geometry"
        Geometry used as the source before buffering.

    Returns
    -------
    geopandas.GeoDataFrame
        A copy of `source_gdf` with nearby polygon area, count, and optional
        category-specific area columns.

    Example
    -------
    >>> from helper.spatial import summarize_polygons_within_distance
    >>> intersections = summarize_polygons_within_distance(
    ...     intersections,
    ...     land_use,
    ...     distance=1320,
    ...     area_column="land_use_acres_nearby",
    ...     category_column="LAND_USE",
    ...     category_area_prefix="nearby_acres_",
    ...     unit="acres",
    ...     projected_epsg=2276,
    ... )
    """
    if distance < 0:
        raise ValueError("distance must be greater than or equal to zero.")

    gpd = require_geodataframes(
        "summarize_polygons_within_distance",
        source_gdf=source_gdf,
        polygon_gdf=polygon_gdf,
    )
    if category_column is not None and category_column not in polygon_gdf.columns:
        raise ValueError(f"category_column was not found: {category_column}")

    square_meter_factor = unit_to_square_meters(unit)
    all_columns = set(source_gdf.columns) | set(polygon_gdf.columns)
    source_id = unique_temp_column(all_columns, "__source_join_id__")
    polygon_id = unique_temp_column(all_columns | {source_id}, "__polygon_join_id__")

    sources = source_gdf.copy()
    polygons = polygon_gdf.copy()
    sources[source_id] = range(len(sources))
    polygons[polygon_id] = range(len(polygons))

    measurement_sources, measurement_polygons = prepare_measurement_crs(
        sources,
        polygons,
        projected_epsg,
        "Nearby polygon summary",
    )
    measurement_sources = set_analysis_geometry(
        measurement_sources,
        source_geometry,
        "summarize_polygons_within_distance",
    )

    result = source_gdf.copy()
    result[source_id] = range(len(result))
    result[area_column] = 0.0
    if count_column is not None:
        result[count_column] = 0

    if measurement_sources.empty or measurement_polygons.empty:
        return result.drop(columns=source_id)

    source_geometry_column = measurement_sources.geometry.name
    polygon_geometry_column = measurement_polygons.geometry.name
    buffers = measurement_sources[[source_id, source_geometry_column]].copy()
    buffers[source_geometry_column] = measurement_sources.geometry.buffer(distance)

    polygon_columns = [polygon_id, polygon_geometry_column]
    if category_column is not None:
        polygon_columns.insert(1, category_column)

    intersections = gpd.overlay(
        buffers[[source_id, source_geometry_column]],
        measurement_polygons[polygon_columns],
        how="intersection",
        keep_geom_type=True,
    )

    if intersections.empty:
        return result.drop(columns=source_id)

    raw_area_column = unique_temp_column(intersections.columns, "__raw_overlap_area__")
    intersections[raw_area_column] = geometry_area_in_square_meters(intersections)
    intersections = intersections[intersections[raw_area_column] > 0].copy()

    if intersections.empty:
        return result.drop(columns=source_id)

    area_summary = intersections.groupby(source_id)[raw_area_column].sum() / square_meter_factor
    result[area_column] = result[source_id].map(area_summary).fillna(0)

    if count_column is not None:
        count_summary = intersections.groupby(source_id)[polygon_id].nunique()
        result[count_column] = result[source_id].map(count_summary).fillna(0).astype(int)

    if category_column is not None:
        category_prefix = category_area_prefix
        if category_prefix is None:
            category_prefix = f"{area_column}_"

        category_values = intersections[category_column].fillna("missing")
        category_summary = (
            intersections.assign(__category_value__=category_values)
            .groupby([source_id, "__category_value__"])[raw_area_column]
            .sum()
            .unstack(fill_value=0)
            / square_meter_factor
        )

        used_columns = set(result.columns)
        for category_value in category_summary.columns:
            output_column = f"{category_prefix}{safe_column_suffix(category_value)}"
            if output_column in used_columns:
                output_column = f"{output_column}_category"

            base_output_column = output_column
            counter = 2
            while output_column in used_columns:
                output_column = f"{base_output_column}_{counter}"
                counter += 1

            used_columns.add(output_column)
            result[output_column] = result[source_id].map(category_summary[category_value]).fillna(0)

    return result.drop(columns=source_id)
