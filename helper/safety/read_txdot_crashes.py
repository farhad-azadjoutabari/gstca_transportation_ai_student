"""Read and clean TxDOT crash CSV files."""

from pathlib import Path


def _normalize_text(value):
    """Normalize column names for loose matching."""
    return "".join(ch for ch in str(value).lower() if ch.isalnum())


def _find_matching_column(columns, candidates):
    """Find the first column that matches one of several candidate names."""
    normalized = {_normalize_text(column): column for column in columns}
    for candidate in candidates:
        key = _normalize_text(candidate)
        if key in normalized:
            return normalized[key]
    return None


def _find_header_row(path, scan_rows, encoding):
    """Find the likely TxDOT header row in a CSV with preamble text."""
    markers = [
        "crashid",
        "crashdate",
        "crashseverity",
        "latitude",
        "longitude",
        "latitudedecimal",
        "longitudedecimal",
    ]

    with open(path, encoding=encoding, errors="replace") as handle:
        for row_number, line in enumerate(handle):
            if row_number >= scan_rows:
                break
            normalized_line = _normalize_text(line)
            score = sum(marker in normalized_line for marker in markers)
            if "crashid" in normalized_line and score >= 2:
                return row_number
            if "latitude" in normalized_line and "longitude" in normalized_line:
                return row_number
    return 0


def read_txdot_crashes(
    file_path,
    header_row="auto",
    scan_rows=50,
    crash_id_column=None,
    latitude_column=None,
    longitude_column=None,
    crs="EPSG:4326",
    deduplicate=True,
    drop_missing_coordinates=True,
    as_geodataframe=True,
    encoding="utf-8-sig",
    **read_csv_kwargs,
):
    """Read a TxDOT crash CSV and return a cleaned table or GeoDataFrame.

    TxDOT crash exports sometimes include title or metadata rows before the
    actual header. This helper searches for the real header row, strips column
    names, removes empty rows/columns, converts crash coordinates to numeric
    values, and optionally builds point geometry.

    Parameters
    ----------
    file_path : str or pathlib.Path
        Path to the TxDOT crash CSV.
    header_row : int or "auto", default "auto"
        Header row passed to pandas. Use "auto" to scan the first `scan_rows`
        rows for the likely header.
    scan_rows : int, default 50
        Number of rows to scan when `header_row="auto"`.
    crash_id_column : str, optional
        Crash ID column. If None, common TxDOT names are detected.
    latitude_column, longitude_column : str, optional
        Coordinate columns. If None, common TxDOT names are detected.
    crs : str or int, default "EPSG:4326"
        CRS assigned to point geometry.
    deduplicate : bool, default True
        If True and a crash ID is available, keep one row per crash ID.
    drop_missing_coordinates : bool, default True
        If True, remove rows without valid latitude/longitude before creating
        geometry.
    as_geodataframe : bool, default True
        If True, return a GeoDataFrame when coordinate columns are available.
    encoding : str, default "utf-8-sig"
        File encoding passed to `pandas.read_csv`.
    **read_csv_kwargs
        Extra options passed to `pandas.read_csv`.

    Returns
    -------
    pandas.DataFrame or geopandas.GeoDataFrame
        Cleaned crash records.

    Example
    -------
    >>> from helper.safety import read_txdot_crashes
    >>> crashes = read_txdot_crashes("data/crashes.csv")
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Crash CSV file not found: {path}")
    if path.suffix.lower() != ".csv":
        raise ValueError(f"Expected a .csv file, but got: {path.name}")

    pd = require_pandas("read_txdot_crashes")

    if header_row == "auto":
        header_row = _find_header_row(path, scan_rows, encoding)
    if header_row is not None and header_row < 0:
        raise ValueError("header_row must be non-negative, None, or 'auto'.")

    read_kwargs = dict(read_csv_kwargs)
    read_kwargs.setdefault("low_memory", False)
    if header_row is None:
        crashes = pd.read_csv(path, encoding=encoding, **read_kwargs)
    else:
        crashes = pd.read_csv(path, skiprows=header_row, encoding=encoding, **read_kwargs)
    crashes.columns = [str(column).strip() for column in crashes.columns]
    crashes = crashes.dropna(axis=1, how="all").dropna(axis=0, how="all").reset_index(drop=True)

    if crash_id_column is None:
        crash_id_column = _find_matching_column(
            crashes.columns,
            ["Crash ID", "Crash_ID", "CRASH_ID", "CrashID", "crash_id"],
        )
    if latitude_column is None:
        latitude_column = _find_matching_column(
            crashes.columns,
            ["Latitude", "LATITUDE", "Lat", "Crash Latitude", "Latitude Decimal"],
        )
    if longitude_column is None:
        longitude_column = _find_matching_column(
            crashes.columns,
            ["Longitude", "LONGITUDE", "Lon", "Long", "Crash Longitude", "Longitude Decimal"],
        )

    if crash_id_column is not None and crash_id_column not in crashes.columns:
        raise ValueError(f"crash_id_column was not found: {crash_id_column}")
    coordinate_columns = [column for column in [latitude_column, longitude_column] if column]
    for column in coordinate_columns:
        if column not in crashes.columns:
            raise ValueError(f"Coordinate column was not found: {column}")
        crashes[column] = pd.to_numeric(crashes[column], errors="coerce")

    if deduplicate and crash_id_column is not None:
        crashes = crashes.drop_duplicates(subset=crash_id_column).reset_index(drop=True)

    has_coordinates = latitude_column is not None and longitude_column is not None
    if has_coordinates and drop_missing_coordinates:
        crashes = crashes.loc[
            crashes[latitude_column].notna() & crashes[longitude_column].notna()
        ].copy()

    if not as_geodataframe or not has_coordinates:
        return crashes

    gpd = require_geopandas("read_txdot_crashes")
    return gpd.GeoDataFrame(
        crashes,
        geometry=gpd.points_from_xy(crashes[longitude_column], crashes[latitude_column]),
        crs=crs,
    )


from ._safety_helpers import require_geopandas, require_pandas
