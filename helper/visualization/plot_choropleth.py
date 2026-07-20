"""Plot a shaded polygon map."""

from .plot_polygons import plot_polygons


def plot_choropleth(
    gdf,
    column,
    cmap="Reds",
    edgecolor="white",
    linewidth=0.5,
    legend=True,
    title=None,
    figsize=(10, 8),
    ax=None,
    **kwargs,
):
    """Draw a choropleth map for polygon data.

    A choropleth shades polygons from light to dark based on a numeric value.
    Use this for tract-level variables such as population, total employers,
    bus stop counts, crash counts, income, or park acres.

    Parameters
    ----------
    gdf : geopandas.GeoDataFrame
        Polygon dataset to draw.
    column : str
        Numeric column used to shade polygons.
    cmap : str, default "Reds"
        Matplotlib color map, such as "Reds", "Blues", "Greens", or "OrRd".
    edgecolor : str, default "white"
        Polygon boundary color.
    linewidth : float, default 0.5
        Polygon boundary width.
    legend : bool, default True
        Whether to show the value legend.
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
    >>> from helper.visualization import plot_choropleth
    >>> ax = plot_choropleth(tracts, "total_employees", cmap="Reds")
    """
    return plot_polygons(
        gdf,
        column=column,
        cmap=cmap,
        edgecolor=edgecolor,
        linewidth=linewidth,
        legend=legend,
        title=title,
        figsize=figsize,
        ax=ax,
        **kwargs,
    )
