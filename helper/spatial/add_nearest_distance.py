"""Add distance to the nearest feature in another spatial dataset."""

from ._access_helpers import normalize_selected_columns, set_analysis_geometry
from ._join_helpers import (
    crs_axis_factor,
    output_column_names,
    require_geodataframes,
    unique_temp_column,
    unit_to_meters,
)


def add_nearest_distance(
    source_gdf,
    target_gdf,
    distance_column="nearest_distance",
    target_columns=None,
    target_prefix="nearest_",
    max_distance=None,
    unit="meters",
    projected_epsg=None,
    source_geometry="geometry",
):
    """Add nearest-target distance and optional target attributes.

    Use this for variables such as distance to the nearest rail station,
    distance to the nearest major road, distance to downtown or employment
    centers, or distance from crashes to the nearest intersection.

    Parameters
    ----------
    source_gdf : geopandas.GeoDataFrame
        Features receiving the nearest-distance column.
    target_gdf : geopandas.GeoDataFrame
        Features to search for nearest neighbors.
    distance_column : str, default "nearest_distance"
        Name of the output distance column.
    target_columns : str, list, or None, default None
        Optional target columns to attach from the nearest feature.
    target_prefix : str, default "nearest_"
        Prefix added to attached target columns.
    max_distance : float, optional
        Maximum search distance in the same units requested by `unit`.
    unit : {"meters", "kilometers", "feet", "miles"}, default "meters"
        Unit for the output distance and `max_distance`.
    projected_epsg : int, optional
        EPSG code to use temporarily for distance calculations.
    source_geometry : {"geometry", "centroid", "representative_point"}, default "geometry"
        Geometry used as the source for nearest-distance search.

    Returns
    -------
    geopandas.GeoDataFrame
        A copy of `source_gdf` with a nearest-distance column and optional
        attributes from the nearest target feature.

    Example
    -------
    >>> from helper.spatial import add_nearest_distance
    >>> tracts = add_nearest_distance(
    ...     tracts,
    ...     rail_stations,
    ...     distance_column="distance_to_nearest_rail_miles",
    ...     unit="miles",
    ...     projected_epsg=2276,
    ...     source_geometry="centroid",
    ... )
    """
    if max_distance is not None and max_distance < 0:
        raise ValueError("max_distance must be greater than or equal to zero.")

    gpd = require_geodataframes(
        "add_nearest_distance",
        source_gdf=source_gdf,
        target_gdf=target_gdf,
    )
    meter_factor = unit_to_meters(unit)

    if source_gdf.crs is None or target_gdf.crs is None:
        raise ValueError("Both GeoDataFrames need CRS values for nearest-distance analysis.")

    available_target_columns = [
        column for column in target_gdf.columns if column != target_gdf.geometry.name
    ]
    selected_columns = normalize_selected_columns(
        target_columns,
        available_target_columns,
        "target_columns",
    )
    renamed_columns = output_column_names(
        selected_columns,
        list(source_gdf.columns) + [distance_column],
        prefix=target_prefix,
        collision_suffix="_nearest",
    )

    result = source_gdf.copy()
    for output_column in renamed_columns.values():
        result[output_column] = None
    result[distance_column] = None

    if source_gdf.empty or target_gdf.empty:
        return result

    all_columns = set(source_gdf.columns) | set(target_gdf.columns) | {distance_column}
    source_id = unique_temp_column(all_columns, "__source_join_id__")
    raw_distance_column = unique_temp_column(all_columns | {source_id}, "__raw_distance__")

    sources = source_gdf.copy()
    targets = target_gdf.rename(columns=renamed_columns).copy()
    sources[source_id] = range(len(sources))

    original_crs = source_gdf.crs
    if projected_epsg is not None:
        measurement_sources = sources.to_crs(epsg=projected_epsg)
        measurement_targets = targets.to_crs(epsg=projected_epsg)
    else:
        measurement_sources = sources
        measurement_targets = (
            targets.to_crs(source_gdf.crs) if source_gdf.crs != target_gdf.crs else targets
        )

    if measurement_sources.crs is not None and measurement_sources.crs.is_geographic:
        raise ValueError("Nearest-distance analysis should use a projected CRS. Pass projected_epsg.")

    measurement_sources = set_analysis_geometry(
        measurement_sources,
        source_geometry,
        "add_nearest_distance",
    )

    axis_factor = crs_axis_factor(measurement_sources.crs)
    search_distance = None
    if max_distance is not None:
        search_distance = max_distance * meter_factor / axis_factor

    target_geometry = measurement_targets.geometry.name
    target_keep_columns = [target_geometry] + list(renamed_columns.values())
    joined = gpd.sjoin_nearest(
        measurement_sources,
        measurement_targets[target_keep_columns],
        how="left",
        max_distance=search_distance,
        distance_col=raw_distance_column,
    )

    sort_columns = [source_id, raw_distance_column]
    if "index_right" in joined.columns:
        sort_columns.append("index_right")
    joined = joined.sort_values(sort_columns, na_position="last").drop_duplicates(source_id)
    joined[distance_column] = joined[raw_distance_column] * axis_factor / meter_factor

    output_columns = [source_id, distance_column] + list(renamed_columns.values())
    result = result.drop(columns=[distance_column] + list(renamed_columns.values()))
    result[source_id] = range(len(result))
    result = result.merge(joined[output_columns], on=source_id, how="left")
    result = result.drop(columns=source_id)

    return result.to_crs(original_crs)
