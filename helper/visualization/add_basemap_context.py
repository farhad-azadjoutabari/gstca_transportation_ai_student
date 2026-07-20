"""Apply common map formatting and optional boundary zoom."""

from ._map_helpers import finish_map, require_geodataframe


def add_basemap_context(
    ax,
    boundary_gdf=None,
    title=None,
    margin=0.03,
    hide_axis=True,
    equal_aspect=True,
):
    """Format a map axis and optionally zoom to a boundary.

    This helper does not download web basemap tiles. It gives student maps a
    clean map frame by hiding axes, keeping equal map scale, adding a title,
    and optionally zooming to the bounds of a boundary GeoDataFrame.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Existing map axis to format.
    boundary_gdf : geopandas.GeoDataFrame, optional
        Dataset used to set the map extent, such as tracts or a county
        boundary.
    title : str, optional
        Map title.
    margin : float, default 0.03
        Fraction of the map width and height added around the boundary.
    hide_axis : bool, default True
        Whether to hide map axes.
    equal_aspect : bool, default True
        Whether to keep equal x and y map scale.

    Returns
    -------
    matplotlib.axes.Axes
        Formatted map axis.

    Example
    -------
    >>> from helper.visualization import add_basemap_context, plot_layers
    >>> ax = plot_layers([{"gdf": tracts}, {"gdf": bus_stops, "type": "point"}])
    >>> ax = add_basemap_context(ax, boundary_gdf=tracts, title="Bus Stops by Tract")
    """
    if boundary_gdf is not None:
        require_geodataframe("add_basemap_context", boundary_gdf)
        minx, miny, maxx, maxy = boundary_gdf.total_bounds
        x_margin = (maxx - minx) * margin
        y_margin = (maxy - miny) * margin
        ax.set_xlim(minx - x_margin, maxx + x_margin)
        ax.set_ylim(miny - y_margin, maxy + y_margin)

    return finish_map(ax, title=title, hide_axis=hide_axis, equal_aspect=equal_aspect)
