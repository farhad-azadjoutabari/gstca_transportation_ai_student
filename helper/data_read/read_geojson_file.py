"""Read GeoJSON files into GeoPandas GeoDataFrames."""

from pathlib import Path


def read_geojson_file(file_path, **kwargs):
    """Read a .geojson file and return a GeoPandas GeoDataFrame.

    Parameters
    ----------
    file_path : str or pathlib.Path
        Path to the GeoJSON file.
    **kwargs
        Optional keyword arguments passed to geopandas.read_file.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"GeoJSON file not found: {path}")

    if path.suffix.lower() not in {".geojson", ".json"}:
        raise ValueError(f"Expected a .geojson or .json file, but got: {path.name}")

    try:
        import geopandas as gpd
    except ImportError as exc:
        raise ImportError(
            "geopandas is required to read GeoJSON files. Install it with: pip install geopandas"
        ) from exc

    return gpd.read_file(path, **kwargs)
