"""Find outliers in numeric columns."""

from ._eda_helpers import numeric_columns, require_pandas


def find_outliers(df, columns=None, method="iqr", threshold=1.5, output_column="is_outlier"):
    """Flag rows with unusual numeric values.

    Use this to identify unusual tracts, road segments, intersections, or
    crashes before modeling. For example, students can flag tracts with very
    high crash counts or roads with unusual congestion values.

    Parameters
    ----------
    df : pandas.DataFrame
        Data table to check.
    columns : list, optional
        Numeric columns to evaluate. If None, all numeric columns are used.
    method : {"iqr", "zscore"}, default "iqr"
        Outlier method. IQR uses quartiles; zscore uses standard deviations.
    threshold : float, default 1.5
        IQR multiplier or absolute z-score threshold.
    output_column : str, default "is_outlier"
        Name of the final any-outlier flag column.

    Returns
    -------
    pandas.DataFrame
        Copy of the input with per-column outlier flags and an overall flag.

    Example
    -------
    >>> from helper.eda import find_outliers
    >>> flagged = find_outliers(tracts, ["crash_count", "total_employees"])
    """
    require_pandas("find_outliers")
    result = df.copy()
    selected = numeric_columns(df, columns)
    flag_columns = []

    for column in selected:
        values = df[column]
        flag_column = f"{column}_outlier"
        if method == "iqr":
            q1 = values.quantile(0.25)
            q3 = values.quantile(0.75)
            iqr = q3 - q1
            lower = q1 - threshold * iqr
            upper = q3 + threshold * iqr
            result[flag_column] = (values < lower) | (values > upper)
        elif method == "zscore":
            std = values.std()
            if std == 0 or values.isna().all():
                result[flag_column] = False
            else:
                result[flag_column] = ((values - values.mean()) / std).abs() > threshold
        else:
            raise ValueError("method must be 'iqr' or 'zscore'.")
        flag_columns.append(flag_column)

    result[output_column] = result[flag_columns].any(axis=1) if flag_columns else False
    return result
