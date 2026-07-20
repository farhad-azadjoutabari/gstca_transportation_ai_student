"""Create a quick map from a GeoDataFrame."""


def quick_plot(gdf, column=None, figsize=(10, 8), legend=True, **kwargs):
    """Make a simple static map for quick visual inspection.

    Use this in notebooks when students want to quickly see whether the data
    loaded correctly, whether the CRS looks reasonable, or how a column varies
    across the map.

    Parameters
    ----------
    gdf : geopandas.GeoDataFrame
        The spatial dataset to map.
    column : str, optional
        Column name used to color the map.
    figsize : tuple, default (10, 8)
        Figure size passed to GeoPandas/Matplotlib.
    legend : bool, default True
        Whether to show a legend when `column` is provided.
    **kwargs
        Additional options passed to GeoDataFrame.plot, such as color,
        edgecolor, linewidth, markersize, or cmap.

    Returns
    -------
    matplotlib.axes.Axes
        The map axes. Students can customize it further if needed.

    Example
    -------
    >>> from helper.data_read import read_shp_file
    >>> from helper.spatial import quick_plot
    >>> crosswalks = read_shp_file("data/crosswalk_city_of_dallas/Crosswalks.shp")
    >>> ax = quick_plot(crosswalks, color="black", markersize=3)
    """
    try:
        import geopandas as gpd
    except ImportError as exc:
        raise ImportError(
            "geopandas is required for spatial helpers. Install it with: pip install geopandas"
        ) from exc

    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise ImportError(
            "matplotlib is required for quick_plot. Install it with: pip install matplotlib"
        ) from exc

    if not isinstance(gdf, gpd.GeoDataFrame):
        raise TypeError("quick_plot expects a geopandas GeoDataFrame.")

    plot_legend = legend if column is not None else False
    ax = gdf.plot(column=column, figsize=figsize, legend=plot_legend, **kwargs)
    ax.set_axis_off()
    plt.tight_layout()

    return ax
