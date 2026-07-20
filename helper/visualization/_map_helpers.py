"""Internal helpers for map visualization functions."""


def require_geodataframe(function_name, gdf):
    """Validate a GeoDataFrame argument and return geopandas."""
    try:
        import geopandas as gpd
    except ImportError as exc:
        raise ImportError(
            "geopandas is required for visualization helpers. Install it with: pip install geopandas"
        ) from exc

    if not isinstance(gdf, gpd.GeoDataFrame):
        raise TypeError(f"{function_name} expects a geopandas GeoDataFrame.")

    return gpd


def require_matplotlib(function_name):
    """Return matplotlib.pyplot with a friendly installation message."""
    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise ImportError(
            f"matplotlib is required for {function_name}. Install it with: pip install matplotlib"
        ) from exc

    return plt


def get_axis(ax, figsize):
    """Return a Matplotlib figure and axis."""
    plt = require_matplotlib("map visualization")
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig = ax.figure
    return fig, ax


def finish_map(ax, title=None, hide_axis=True, equal_aspect=True):
    """Apply common map formatting."""
    if title:
        ax.set_title(title)
    if hide_axis:
        ax.set_axis_off()
    if equal_aspect:
        ax.set_aspect("equal", adjustable="box")
    return ax


def check_geometry_family(gdf, function_name, allowed_types):
    """Raise a helpful error when a plot function gets the wrong geometry type."""
    geometry_types = set(gdf.geometry.geom_type.dropna().unique())
    if not geometry_types:
        return

    bad_types = sorted(geometry_types - set(allowed_types))
    if bad_types:
        allowed = ", ".join(allowed_types)
        found = ", ".join(sorted(geometry_types))
        raise ValueError(f"{function_name} expects {allowed} geometry, but found: {found}.")


def plot_with_optional_column(
    gdf,
    ax,
    column=None,
    color=None,
    cmap=None,
    legend=True,
    missing_color="lightgray",
    **kwargs,
):
    """Plot a GeoDataFrame with either a data column or a fixed color."""
    plot_kwargs = dict(kwargs)

    if column is None:
        if color is not None:
            plot_kwargs["color"] = color
        return gdf.plot(ax=ax, **plot_kwargs)

    if column not in gdf.columns:
        raise ValueError(f"Column was not found: {column}")

    plot_kwargs["column"] = column
    plot_kwargs["legend"] = legend
    if cmap is not None:
        plot_kwargs["cmap"] = cmap
    plot_kwargs.setdefault("missing_kwds", {"color": missing_color})
    return gdf.plot(ax=ax, **plot_kwargs)


def align_to_base_crs(gdf, base_crs):
    """Reproject a layer to the base CRS when both CRS values are known."""
    if base_crs is not None and gdf.crs is not None and gdf.crs != base_crs:
        return gdf.to_crs(base_crs)
    return gdf


def infer_geometry_kind(gdf):
    """Infer whether a GeoDataFrame mostly contains points, lines, or polygons."""
    geometry_types = set(gdf.geometry.geom_type.dropna().unique())
    if geometry_types <= {"Point", "MultiPoint"}:
        return "point"
    if geometry_types <= {"LineString", "MultiLineString", "LinearRing"}:
        return "line"
    if geometry_types <= {"Polygon", "MultiPolygon"}:
        return "polygon"
    return "geometry"
