"""Plot point spatial data."""

from ._map_helpers import (
    check_geometry_family,
    finish_map,
    get_axis,
    plot_with_optional_column,
    require_geodataframe,
)


def plot_points(
    gdf,
    column=None,
    color="black",
    cmap="viridis",
    markersize=20,
    alpha=0.8,
    legend=True,
    title=None,
    figsize=(10, 8),
    ax=None,
    **kwargs,
):
    """Draw point features on a map.

    Use this for point layers such as bus stops, employers, developments,
    crashes, rail stations, EV charging stations, signals, or signs. If
    `column` is provided, points are colored by that data value.

    Parameters
    ----------
    gdf : geopandas.GeoDataFrame
        Point dataset to draw.
    column : str, optional
        Column used to color points by value or category.
    color : str, default "black"
        Fixed point color used when `column` is None.
    cmap : str, default "viridis"
        Matplotlib color map used when `column` is provided.
    markersize : float or str, default 20
        Fixed marker size, or a column name containing marker sizes.
    alpha : float, default 0.8
        Point transparency, from 0 to 1.
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
    >>> from helper.visualization import plot_points
    >>> ax = plot_points(bus_stops, color="black", markersize=8)
    """
    require_geodataframe("plot_points", gdf)
    check_geometry_family(gdf, "plot_points", {"Point", "MultiPoint"})
    _, ax = get_axis(ax, figsize)

    plot_with_optional_column(
        gdf,
        ax,
        column=column,
        color=color,
        cmap=cmap,
        legend=legend,
        markersize=markersize,
        alpha=alpha,
        **kwargs,
    )
    return finish_map(ax, title=title)
