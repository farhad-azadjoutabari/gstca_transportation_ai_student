"""Create side-by-side comparison maps."""

from ._map_helpers import align_to_base_crs, finish_map, get_axis, plot_with_optional_column
from ._map_helpers import require_geodataframe, require_matplotlib


def plot_before_after(
    before_gdf,
    after_gdf,
    before_column=None,
    after_column=None,
    titles=("Before", "After"),
    cmap="Reds",
    color="lightgray",
    figsize=(14, 6),
    legend=True,
    **kwargs,
):
    """Draw two spatial maps side by side.

    Use this to compare two stages of work, such as raw data and joined data,
    before and after a filter, or current and future scenarios.

    Parameters
    ----------
    before_gdf : geopandas.GeoDataFrame
        Dataset shown on the left.
    after_gdf : geopandas.GeoDataFrame
        Dataset shown on the right.
    before_column : str, optional
        Column used to shade or color the left map.
    after_column : str, optional
        Column used to shade or color the right map.
    titles : tuple, default ("Before", "After")
        Titles for the left and right maps.
    cmap : str, default "Reds"
        Matplotlib color map used when columns are provided.
    color : str, default "lightgray"
        Fixed color used when a column is not provided.
    figsize : tuple, default (14, 6)
        Figure size.
    legend : bool, default True
        Whether to show legends when columns are provided.
    **kwargs
        Extra options passed to GeoDataFrame.plot.

    Returns
    -------
    tuple
        `(fig, axes)` from Matplotlib.

    Example
    -------
    >>> from helper.visualization import plot_before_after
    >>> fig, axes = plot_before_after(tracts, tracts_joined, after_column="bus_stop_count")
    """
    require_geodataframe("plot_before_after", before_gdf)
    require_geodataframe("plot_before_after", after_gdf)
    plt = require_matplotlib("plot_before_after")

    fig, axes = plt.subplots(1, 2, figsize=figsize)
    after = align_to_base_crs(after_gdf, before_gdf.crs)

    plot_with_optional_column(
        before_gdf,
        axes[0],
        column=before_column,
        color=color,
        cmap=cmap,
        legend=legend,
        **kwargs,
    )
    plot_with_optional_column(
        after,
        axes[1],
        column=after_column,
        color=color,
        cmap=cmap,
        legend=legend,
        **kwargs,
    )

    finish_map(axes[0], title=titles[0] if titles else None)
    finish_map(axes[1], title=titles[1] if titles else None)
    plt.tight_layout()

    return fig, axes
