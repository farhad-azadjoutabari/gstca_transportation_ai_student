"""Save a Matplotlib map figure."""

from pathlib import Path

from ._map_helpers import require_matplotlib


def save_map(fig, output_path, dpi=300, bbox_inches="tight", transparent=False, **kwargs):
    """Save a map figure to an image or PDF file.

    Use this after making a map in a notebook so students can include it in a
    report, slide deck, or project folder.

    Parameters
    ----------
    fig : matplotlib.figure.Figure or None
        Figure to save. If None, the current Matplotlib figure is saved.
    output_path : str or pathlib.Path
        Output path ending in `.png`, `.jpg`, `.jpeg`, `.pdf`, or `.svg`.
    dpi : int, default 300
        Image resolution.
    bbox_inches : str, default "tight"
        Bounding box option passed to `savefig`.
    transparent : bool, default False
        Whether to save with a transparent background.
    **kwargs
        Extra options passed to Matplotlib `savefig`.

    Returns
    -------
    pathlib.Path
        Path to the saved map file.

    Example
    -------
    >>> from helper.visualization import plot_choropleth, save_map
    >>> ax = plot_choropleth(tracts, "total_employees")
    >>> save_map(ax.figure, "outputs/total_employees_map.png")
    """
    plt = require_matplotlib("save_map")
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".pdf", ".svg"}:
        raise ValueError("Use an output path ending in .png, .jpg, .jpeg, .pdf, or .svg.")

    figure = fig if fig is not None else plt.gcf()
    figure.savefig(
        path,
        dpi=dpi,
        bbox_inches=bbox_inches,
        transparent=transparent,
        **kwargs,
    )
    return path
