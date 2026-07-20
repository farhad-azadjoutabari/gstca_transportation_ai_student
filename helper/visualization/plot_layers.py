"""Plot multiple spatial layers on one map."""

from ._map_helpers import (
    align_to_base_crs,
    finish_map,
    get_axis,
    infer_geometry_kind,
    plot_with_optional_column,
    require_geodataframe,
)


def plot_layers(layers, title=None, figsize=(10, 8), ax=None, hide_axis=True):
    """Draw multiple GeoDataFrames on one map.

    Use this when students want to overlay several shapefiles, such as tracts
    in the background, bus routes as lines, and bus stops as points. Each
    layer is described with a dictionary.

    Parameters
    ----------
    layers : list of dict
        Layer settings. Each dictionary must include `gdf`. Optional keys
        include `type`, `column`, `color`, `cmap`, `legend`, `markersize`,
        `linewidth`, `edgecolor`, `alpha`, and any GeoDataFrame.plot option.
    title : str, optional
        Map title.
    figsize : tuple, default (10, 8)
        Figure size when `ax` is not provided.
    ax : matplotlib.axes.Axes, optional
        Existing axis to draw on.
    hide_axis : bool, default True
        Whether to hide map axes.

    Returns
    -------
    matplotlib.axes.Axes
        Map axis.

    Example
    -------
    >>> from helper.visualization import plot_layers
    >>> ax = plot_layers([
    ...     {"gdf": tracts, "type": "polygon", "column": "total_employees", "cmap": "Reds"},
    ...     {"gdf": bus_routes, "type": "line", "color": "blue", "linewidth": 1},
    ...     {"gdf": bus_stops, "type": "point", "color": "black", "markersize": 8},
    ... ])
    """
    if not layers:
        raise ValueError("plot_layers expects at least one layer.")

    _, ax = get_axis(ax, figsize)

    base_crs = None
    for layer in layers:
        if "gdf" not in layer:
            raise ValueError("Each layer dictionary must include a 'gdf' value.")
        gdf = layer["gdf"]
        require_geodataframe("plot_layers", gdf)
        if base_crs is None and gdf.crs is not None:
            base_crs = gdf.crs

    for layer in layers:
        options = dict(layer)
        gdf = align_to_base_crs(options.pop("gdf"), base_crs)
        layer_type = options.pop("type", options.pop("kind", None))
        if layer_type is None:
            layer_type = infer_geometry_kind(gdf)
        else:
            layer_type = str(layer_type).lower()
            type_aliases = {
                "points": "point",
                "lines": "line",
                "links": "line",
                "link": "line",
                "polygons": "polygon",
            }
            layer_type = type_aliases.get(layer_type, layer_type)

        column = options.pop("column", None)
        cmap = options.pop("cmap", "viridis")
        legend = options.pop("legend", column is not None)
        alpha = options.pop("alpha", 1.0)

        if layer_type == "polygon":
            options.setdefault("edgecolor", "white")
            options.setdefault("linewidth", 0.5)
            options.setdefault("color", "lightgray")
        elif layer_type == "line":
            options.setdefault("linewidth", 1.5)
            options.setdefault("color", "black")
        elif layer_type == "point":
            options.setdefault("markersize", 20)
            options.setdefault("color", "black")

        color = options.pop("color", None)
        plot_with_optional_column(
            gdf,
            ax,
            column=column,
            color=color,
            cmap=cmap,
            legend=legend,
            alpha=alpha,
            **options,
        )

    return finish_map(ax, title=title, hide_axis=hide_axis)
