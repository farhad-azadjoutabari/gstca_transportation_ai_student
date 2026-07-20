"""Read GeoPackage files into GeoPandas GeoDataFrames."""

from pathlib import Path


def read_gpkg_file(file_path, layer=None, **kwargs):
    """Read a .gpkg file and return a GeoPandas GeoDataFrame.

    Parameters
    ----------
    file_path : str or pathlib.Path
        Path to the GeoPackage file.
    layer : str, optional
        Layer name to read when the GeoPackage contains multiple layers.
    **kwargs
        Optional keyword arguments passed to geopandas.read_file.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"GeoPackage file not found: {path}")

    if path.suffix.lower() != ".gpkg":
        raise ValueError(f"Expected a .gpkg file, but got: {path.name}")

    try:
        import geopandas as gpd
    except ImportError as exc:
        raise ImportError(
            "geopandas is required to read GeoPackage files. Install it with: pip install geopandas"
        ) from exc

    if layer is None:
        return gpd.read_file(path, **kwargs)

    return gpd.read_file(path, layer=layer, **kwargs)
