"""Read shapefiles into GeoPandas GeoDataFrames."""

from pathlib import Path


def read_shp_file(file_path, **kwargs):
    """Read a .shp shapefile and return a GeoPandas GeoDataFrame.

    Parameters
    ----------
    file_path : str or pathlib.Path
        Path to the .shp file.
    **kwargs
        Optional keyword arguments passed to geopandas.read_file.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Shapefile not found: {path}")

    if path.suffix.lower() != ".shp":
        raise ValueError(f"Expected a .shp file, but got: {path.name}")

    try:
        import geopandas as gpd
    except ImportError as exc:
        raise ImportError(
            "geopandas is required to read shapefiles. Install it with: pip install geopandas"
        ) from exc

    return gpd.read_file(path, **kwargs)
