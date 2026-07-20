"""Calculate polygon coverage by buffered facilities."""

from ._join_helpers import (
    crs_axis_factor,
    prepare_measurement_crs,
    require_geodataframes,
    unit_to_square_meters,
)


def calculate_facility_coverage(
    polygon_gdf,
    facility_gdf,
    buffer_distance,
    coverage_area_column="facility_coverage_area",
    coverage_percent_column="facility_coverage_percent",
    unit="square_meters",
    projected_epsg=None,
):
    """Calculate how much of each polygon is covered by nearby facilities.

    Use this for variables such as percent of a tract within a half mile of a
    transit stop, percent of a neighborhood within a quarter mile of bikeways,
    or acres covered by parks, school zones, rail station buffers, or EV
    charging access buffers.

    Facility buffers are unioned before measuring coverage, so overlapping
    buffers are not double-counted.

    Parameters
    ----------
    polygon_gdf : geopandas.GeoDataFrame
        Polygon dataset receiving the coverage columns, such as tracts or
        neighborhoods.
    facility_gdf : geopandas.GeoDataFrame
        Facility features to buffer. Points, lines, and polygons are accepted.
    buffer_distance : float
        Facility buffer distance in the units of the projected CRS. Use 0 when
        `facility_gdf` already contains service-area polygons.
    coverage_area_column : str, default "facility_coverage_area"
        Name of the output covered-area column.
    coverage_percent_column : str or None, default "facility_coverage_percent"
        Name of the output percent-covered column. Set to None to skip it.
    unit : {"square_meters", "square_kilometers", "square_feet", "square_miles", "acres"}, default "square_meters"
        Unit for the covered-area column.
    projected_epsg : int, optional
        EPSG code to use temporarily for buffering and area calculations.

    Returns
    -------
    geopandas.GeoDataFrame
        A copy of `polygon_gdf` with facility coverage columns.

    Example
    -------
    >>> from helper.spatial import calculate_facility_coverage
    >>> tracts = calculate_facility_coverage(
    ...     tracts,
    ...     bus_stops,
    ...     buffer_distance=2640,
    ...     coverage_area_column="transit_access_acres",
    ...     coverage_percent_column="pct_tract_near_transit",
    ...     unit="acres",
    ...     projected_epsg=2276,
    ... )
    """
    if buffer_distance < 0:
        raise ValueError("buffer_distance must be greater than or equal to zero.")

    require_geodataframes(
        "calculate_facility_coverage",
        polygon_gdf=polygon_gdf,
        facility_gdf=facility_gdf,
    )
    square_meter_factor = unit_to_square_meters(unit)

    measurement_polygons, measurement_facilities = prepare_measurement_crs(
        polygon_gdf,
        facility_gdf,
        projected_epsg,
        "Facility coverage",
    )

    result = polygon_gdf.copy()
    result[coverage_area_column] = 0.0
    if coverage_percent_column is not None:
        result[coverage_percent_column] = 0.0

    if measurement_polygons.empty or measurement_facilities.empty:
        return result

    facility_buffers = measurement_facilities.geometry.buffer(buffer_distance)
    facility_buffers = facility_buffers[~facility_buffers.is_empty]
    if facility_buffers.empty:
        return result

    if hasattr(facility_buffers, "union_all"):
        coverage_geometry = facility_buffers.union_all()
    else:
        coverage_geometry = facility_buffers.unary_union

    factor = crs_axis_factor(measurement_polygons.crs)
    covered_area_square_meters = (
        measurement_polygons.geometry.intersection(coverage_geometry).area * (factor**2)
    )
    polygon_area_square_meters = measurement_polygons.geometry.area * (factor**2)

    result[coverage_area_column] = covered_area_square_meters / square_meter_factor

    if coverage_percent_column is not None:
        denominator = polygon_area_square_meters.replace(0, float("nan"))
        result[coverage_percent_column] = (
            covered_area_square_meters / denominator * 100
        ).fillna(0)

    return result
