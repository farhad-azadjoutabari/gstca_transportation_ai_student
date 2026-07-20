"""Plot spatial data by category."""

from ._map_helpers import finish_map, get_axis, plot_with_optional_column, require_geodataframe


def plot_categorical_map(
    gdf,
    column,
    cmap="tab20",
    legend=True,
    title=None,
    figsize=(10, 8),
    ax=None,
    **kwargs,
):
    """Draw a map where each category gets a different color.

    Use this for text or class columns such as congestion severity, land-use
    type, development status, facility type, road class, or transit zone name.
    This function works with point, line, and polygon GeoDataFrames.

    Parameters
    ----------
    gdf : geopandas.GeoDataFrame
        Spatial dataset to draw.
    column : str
        Category column used for colors.
    cmap : str, default "tab20"
        Matplotlib categorical color map.
    legend : bool, default True
        Whether to show the category legend.
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
    >>> from helper.visualization import plot_categorical_map
    >>> ax = plot_categorical_map(congestion, "severity")
    """
    require_geodataframe("plot_categorical_map", gdf)
    _, ax = get_axis(ax, figsize)

    plot_with_optional_column(
        gdf,
        ax,
        column=column,
        cmap=cmap,
        legend=legend,
        categorical=True,
        **kwargs,
    )
    return finish_map(ax, title=title)
