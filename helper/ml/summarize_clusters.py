"""Summarize cluster characteristics."""

from ._ml_helpers import check_columns, normalize_columns, require_pandas


def summarize_clusters(df, cluster_column="cluster", feature_columns=None, include_count=True):
    """Summarize average feature values by cluster.

    Use this after adding cluster labels back to a tract or record table. It
    helps students explain what each cluster means, such as "high employment,
    low transit access" or "low income, high crash count."

    Parameters
    ----------
    df : pandas.DataFrame
        Data table containing cluster labels and feature columns.
    cluster_column : str, default "cluster"
        Column containing cluster labels.
    feature_columns : list, optional
        Numeric columns to summarize. If None, all numeric columns except the
        cluster column are summarized.
    include_count : bool, default True
        Whether to include the number of records in each cluster.

    Returns
    -------
    pandas.DataFrame
        Cluster summary table.

    Example
    -------
    >>> from helper.ml import summarize_clusters
    >>> tracts["cluster"] = result["labels"]
    >>> cluster_summary = summarize_clusters(tracts, cluster_column="cluster")
    """
    pd = require_pandas("summarize_clusters")
    if cluster_column not in df.columns:
        raise ValueError(f"cluster_column was not found: {cluster_column}")

    if feature_columns is None:
        feature_columns = [
            column
            for column in df.select_dtypes(include="number").columns
            if column != cluster_column
        ]
    else:
        feature_columns = normalize_columns(feature_columns, "feature_columns")
        check_columns(df, feature_columns, "feature_columns")

    summary = df.groupby(cluster_column)[feature_columns].mean()
    if include_count:
        counts = df.groupby(cluster_column).size().rename("record_count")
        summary = pd.concat([counts, summary], axis=1)

    return summary.reset_index()
