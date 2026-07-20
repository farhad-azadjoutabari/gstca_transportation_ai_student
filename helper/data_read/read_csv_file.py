"""Read CSV files into pandas DataFrames."""

from pathlib import Path


def read_csv_file(file_path, **kwargs):
    """Read a .csv file and return a pandas DataFrame.

    Parameters
    ----------
    file_path : str or pathlib.Path
        Path to the CSV file.
    **kwargs
        Optional keyword arguments passed to pandas.read_csv.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")

    if path.suffix.lower() != ".csv":
        raise ValueError(f"Expected a .csv file, but got: {path.name}")

    try:
        import pandas as pd
    except ImportError as exc:
        raise ImportError(
            "pandas is required to read CSV files. Install it with: pip install pandas"
        ) from exc

    return pd.read_csv(path, **kwargs)
