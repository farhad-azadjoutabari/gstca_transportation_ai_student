"""Plot line spatial data."""

from ._map_helpers import (
    check_geometry_family,
    finish_map,
    get_axis,
    plot_with_optional_column,
    require_geodataframe,
)


def plot_lines(
    gdf,
    column=None,
    color="black",
    cmap="viridis",
    linewidth=1.5,
    alpha=0.9,
    legend=True,
    title=None,
    figsize=(10, 8),
    ax=None,
    **kwargs,
):
    """Draw line features on a map.

    Use this for line or link layers such as roads, bus routes, bikeways,
    trails, truck restrictions, speed-limit segments, or network links. If
    `column` is provided, lines are colored by that data value.

    Parameters
    ----------
    gdf : geopandas.GeoDataFrame
        Line dataset to draw.
    column : str, optional
        Column used to color lines by value or category.
    color : str, default "black"
        Fixed line color used when `column` is None.
    cmap : str, default "viridis"
        Matplotlib color map used when `column` is provided.
    linewidth : float, default 1.5
        Line width.
    alpha : float, default 0.9
        Line transparency, from 0 to 1.
    legend : bool, default True
        Whether to show a legend when `column` is provided.
    title : str, optional
        Map title.
    figsize : tuple, default (10, 8)
        Figure size when `ax` is not provided.
    ax : matplotlib.axes.Axes, optional
        Existing axis to draw on.
    **kwargs
        Extra options passed to GeoDataFrame.plot.

    Returns
    -------
    matplotlib.axes.Axes
        Map axis.

    Example
    -------
    >>> from helper.visualization import plot_lines
    >>> ax = plot_lines(bus_routes, color="blue", linewidth=1)
    """
    require_geodataframe("plot_lines", gdf)
    check_geometry_family(gdf, "plot_lines", {"LineString", "MultiLineString", "LinearRing"})
    _, ax = get_axis(ax, figsize)

    plot_with_optional_column(
        gdf,
        ax,
        column=column,
        color=color,
        cmap=cmap,
        legend=legend,
        linewidth=linewidth,
        alpha=alpha,
        **kwargs,
    )
    return finish_map(ax, title=title)
