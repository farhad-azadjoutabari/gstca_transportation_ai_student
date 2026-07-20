"""Attach nearest-feature distances and attributes from one or more layers."""

import re

from .add_nearest_distance import add_nearest_distance
from ._join_helpers import require_geodataframes


def _safe_name(value):
    """Create a simple column-name fragment."""
    name = re.sub(r"[^0-9a-zA-Z]+", "_", str(value).strip().lower()).strip("_")
    return name or "feature"


def _target_specs(targets):
    """Normalize nearest-feature specifications."""
    if isinstance(targets, dict):
        if "gdf" in targets:
            return [dict(targets)]
        return [{"name": name, "gdf": gdf} for name, gdf in targets.items()]

    specs = []
    for item in targets:
        if isinstance(item, dict):
            specs.append(dict(item))
        elif isinstance(item, (list, tuple)) and len(item) == 2:
            specs.append({"name": item[0], "gdf": item[1]})
        else:
            raise TypeError(
                "targets must be a dictionary, a list of dictionaries, or "
                "a list of (name, GeoDataFrame) pairs."
            )
    return specs


def attach_nearest_features(
    source_gdf,
    targets,
    projected_epsg=None,
    unit="meters",
    source_geometry="geometry",
):
    """Attach nearest distances and optional target attributes from many layers.

    This is a convenience wrapper around `add_nearest_distance`. It is useful
    when students want to enrich the same tract, road, or intersection table
    with several proximity variables, such as nearest rail station, nearest
    major road, nearest signal, nearest employment center, and nearest park.

    Parameters
    ----------
    source_gdf : geopandas.GeoDataFrame
        Features receiving the new nearest-feature columns.
    targets : dict or list
        Target layers. A dictionary can map names to GeoDataFrames. A list can
        contain dictionaries with keys such as `name`, `gdf`, `columns`,
        `distance_column`, `target_prefix`, `unit`, `max_distance`, and
        `source_geometry`.
    projected_epsg : int, optional
        EPSG code used temporarily for distance calculations.
    unit : {"meters", "kilometers", "feet", "miles"}, default "meters"
        Default distance unit for all targets unless a target overrides it.
    source_geometry : {"geometry", "centroid", "representative_point"}, default "geometry"
        Default source geometry for nearest-distance search unless a target
        overrides it.

    Returns
    -------
    geopandas.GeoDataFrame
        Copy of `source_gdf` with nearest-distance and optional target
        attribute columns added.

    Example
    -------
    >>> from helper.spatial import attach_nearest_features
    >>> tracts = attach_nearest_features(
    ...     tracts,
    ...     {
    ...         "rail_station": rail_stations,
    ...         "major_road": major_roads,
    ...     },
    ...     projected_epsg=2276,
    ...     unit="miles",
    ...     source_geometry="centroid",
    ... )
    """
    require_geodataframes("attach_nearest_features", source_gdf=source_gdf)
    result = source_gdf.copy()

    for spec in _target_specs(targets):
        if "gdf" not in spec:
            raise ValueError("Each target specification must include a 'gdf' value.")
        target_gdf = spec["gdf"]
        require_geodataframes("attach_nearest_features", target_gdf=target_gdf)

        name = _safe_name(spec.get("name", "feature"))
        target_unit = spec.get("unit", unit)
        distance_column = spec.get("distance_column", f"nearest_{name}_distance_{target_unit}")
        target_prefix = spec.get("target_prefix", f"nearest_{name}_")

        result = add_nearest_distance(
            result,
            target_gdf,
            distance_column=distance_column,
            target_columns=spec.get("columns", spec.get("target_columns")),
            target_prefix=target_prefix,
            max_distance=spec.get("max_distance"),
            unit=target_unit,
            projected_epsg=spec.get("projected_epsg", projected_epsg),
            source_geometry=spec.get("source_geometry", source_geometry),
        )

    return result
