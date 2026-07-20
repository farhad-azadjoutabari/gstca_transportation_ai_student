"""Prepare a GeoDataFrame for spatial joins and measurements."""

import warnings

from ._join_helpers import require_geodataframes


def prepare_spatial_data(
    gdf,
    input_crs=None,
    projected_epsg=None,
    geometry_column=None,
    drop_empty=True,
    make_valid=False,
    warn_if_geographic=True,
    reset_index=True,
    override_crs=False,
):
    """Clean CRS and geometry issues before spatial analysis.

    Use this helper before buffers, nearest-distance joins, area calculations,
    or length calculations. It can assign a missing CRS, switch the active
    geometry column, drop missing/empty geometries, optionally repair invalid
    polygons, and project the data to a local CRS.

    Parameters
    ----------
    gdf : geopandas.GeoDataFrame
        Spatial dataset to prepare.
    input_crs : str, int, or None, default None
        CRS to assign when the GeoDataFrame has no CRS. If `override_crs=True`,
        this CRS replaces the existing CRS.
    projected_epsg : int or None, default None
        Optional EPSG code to project to after CRS assignment.
    geometry_column : str or None, default None
        Optional column to set as the active geometry.
    drop_empty : bool, default True
        Remove rows with missing or empty geometry.
    make_valid : bool, default False
        Attempt to repair invalid geometries when GeoPandas/Shapely supports
        it.
    warn_if_geographic : bool, default True
        Warn when the result is still in longitude/latitude coordinates.
    reset_index : bool, default True
        Reset row index after dropping empty geometries.
    override_crs : bool, default False
        If True, assign `input_crs` even when the input already has a CRS.

    Returns
    -------
    geopandas.GeoDataFrame
        Prepared copy of the input GeoDataFrame.

    Example
    -------
    >>> from helper.spatial import prepare_spatial_data
    >>> roads = prepare_spatial_data(roads, input_crs=4326, projected_epsg=2276)
    """
    require_geodataframes("prepare_spatial_data", gdf=gdf)

    result = gdf.copy()
    if geometry_column is not None:
        if geometry_column not in result.columns:
            raise ValueError(f"geometry_column was not found: {geometry_column}")
        result = result.set_geometry(geometry_column)

    if input_crs is not None:
        if result.crs is None or override_crs:
            result = result.set_crs(input_crs, allow_override=override_crs)
    elif result.crs is None:
        raise ValueError(
            "This GeoDataFrame has no CRS. Pass input_crs, such as input_crs=4326."
        )

    if drop_empty:
        keep_rows = result.geometry.notna() & ~result.geometry.is_empty
        result = result.loc[keep_rows].copy()
        if reset_index:
            result = result.reset_index(drop=True)

    if make_valid:
        try:
            result.geometry = result.geometry.make_valid()
        except AttributeError:
            result.geometry = result.geometry.buffer(0)

    if projected_epsg is not None:
        result = result.to_crs(epsg=projected_epsg)

    if warn_if_geographic and result.crs is not None and result.crs.is_geographic:
        warnings.warn(
            "This GeoDataFrame is still in a geographic CRS. Distance, length, "
            "area, and buffer calculations should use a projected CRS such as "
            "EPSG:2276 for Dallas-area work.",
            UserWarning,
            stacklevel=2,
        )

    return result
