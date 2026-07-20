"""Plot polygon spatial data."""

from ._map_helpers import (
    check_geometry_family,
    finish_map,
    get_axis,
    plot_with_optional_column,
    require_geodataframe,
)


def plot_polygons(
    gdf,
    column=None,
    color="lightgray",
    cmap="Reds",
    edgecolor="white",
    linewidth=0.5,
    alpha=1.0,
    legend=True,
    title=None,
    figsize=(10, 8),
    ax=None,
    **kwargs,
):
    """Draw polygon features on a map.

    Use this for polygon layers such as Census tracts, parks, land-use areas,
    airports, congestion zones, or service areas. If `column` is provided, the
    polygons are shaded by that data value.

    Parameters
    ----------
    gdf : geopandas.GeoDataFrame
        Polygon dataset to draw.
    column : str, optional
        Column used to shade polygons by value.
    color : str, default "lightgray"
        Fixed polygon fill color used when `column` is None.
    cmap : str, default "Reds"
        Matplotlib color map used when `column` is provided.
    edgecolor : str, default "white"
        Polygon boundary color.
    linewidth : float, default 0.5
        Polygon boundary width.
    alpha : float, default 1.0
        Polygon transparency, from 0 to 1.
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
    >>> from helper.visualization import plot_polygons
    >>> ax = plot_polygons(tracts, column="total_employees", cmap="Reds")
    """
    require_geodataframe("plot_polygons", gdf)
    check_geometry_family(gdf, "plot_polygons", {"Polygon", "MultiPolygon"})
    _, ax = get_axis(ax, figsize)

    plot_with_optional_column(
        gdf,
        ax,
        column=column,
        color=color,
        cmap=cmap,
        legend=legend,
        edgecolor=edgecolor,
        linewidth=linewidth,
        alpha=alpha,
        **kwargs,
    )
    return finish_map(ax, title=title)
