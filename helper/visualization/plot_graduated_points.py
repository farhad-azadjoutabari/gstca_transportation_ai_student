"""Plot points with marker size based on a value."""

from ._map_helpers import check_geometry_family, finish_map, get_axis, require_geodataframe


def plot_graduated_points(
    gdf,
    size_column,
    color_column=None,
    color="black",
    cmap="viridis",
    min_size=20,
    max_size=250,
    alpha=0.75,
    legend=True,
    title=None,
    figsize=(10, 8),
    ax=None,
    **kwargs,
):
    """Draw points with larger markers for larger values.

    Use this for point layers where size matters, such as employer jobs,
    apartment units, crash counts, development size, or station activity. A
    separate `color_column` can also color points by value or category.

    Parameters
    ----------
    gdf : geopandas.GeoDataFrame
        Point dataset to draw.
    size_column : str
        Numeric column used to scale marker sizes.
    color_column : str, optional
        Column used to color points.
    color : str, default "black"
        Fixed point color used when `color_column` is None.
    cmap : str, default "viridis"
        Matplotlib color map used when `color_column` is provided.
    min_size : float, default 20
        Marker size for the smallest value.
    max_size : float, default 250
        Marker size for the largest value.
    alpha : float, default 0.75
        Point transparency, from 0 to 1.
    legend : bool, default True
        Whether to show a color legend when `color_column` is provided.
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
    >>> from helper.visualization import plot_graduated_points
    >>> ax = plot_graduated_points(employers, size_column="EMPLOYEES")
    """
    require_geodataframe("plot_graduated_points", gdf)
    check_geometry_family(gdf, "plot_graduated_points", {"Point", "MultiPoint"})
    if size_column not in gdf.columns:
        raise ValueError(f"size_column was not found: {size_column}")
    if color_column is not None and color_column not in gdf.columns:
        raise ValueError(f"color_column was not found: {color_column}")

    import pandas as pd

    _, ax = get_axis(ax, figsize)
    values = pd.to_numeric(gdf[size_column], errors="coerce").fillna(0)
    value_min = values.min()
    value_max = values.max()

    if value_max == value_min:
        marker_sizes = values * 0 + ((min_size + max_size) / 2)
    else:
        marker_sizes = min_size + (values - value_min) / (value_max - value_min) * (
            max_size - min_size
        )

    plot_kwargs = dict(kwargs)
    plot_kwargs["markersize"] = marker_sizes
    plot_kwargs["alpha"] = alpha

    if color_column is None:
        plot_kwargs["color"] = color
    else:
        plot_kwargs["column"] = color_column
        plot_kwargs["cmap"] = cmap
        plot_kwargs["legend"] = legend

    gdf.plot(ax=ax, **plot_kwargs)
    return finish_map(ax, title=title)
