# DBSCAN Clustering

DBSCAN is a clustering algorithm that finds dense groups of points and labels sparse points as outliers.

DBSCAN stands for Density-Based Spatial Clustering of Applications with Noise.

In this project, DBSCAN clusters rows based on similarity in prepared feature space. It is not automatically geographic clustering unless latitude, longitude, or spatial features are included in the feature table.

## When To Use It

Use DBSCAN when:

- You want clusters based on density.
- You do not want to choose the number of clusters in advance.
- You want to identify unusual records or outliers.
- Clusters may have irregular shapes.

Transportation examples:

- Detect unusual tracts based on demographics and access features.
- Find dense groups of similar road segments.
- Identify intersections that do not fit common safety/exposure patterns.

## Main Idea

DBSCAN looks at neighborhoods around each row:

- `eps`: how far away another row can be and still count as nearby.
- `min_samples`: how many nearby rows are needed to form a dense area.

Rows in dense areas become clusters. Rows that are not part of any dense area get label `-1`, which means noise or outlier.

## Helper Function

Use:

```python
from helper.ml import run_dbscan_clustering, evaluate_clustering, summarize_clusters
```

Implementation file:

```text
helper/ml/run_dbscan_clustering.py
```

Inside the helper, `run_dbscan_clustering` creates scikit-learn `DBSCAN`.

## Example

```python
from helper.ml import (
    prepare_ml_data,
    run_dbscan_clustering,
    evaluate_clustering,
    summarize_clusters,
)

features = [
    "population_density",
    "employment_density",
    "median_income",
    "bus_stop_count",
    "land_use_mix",
]

cluster_data = prepare_ml_data(
    tracts,
    feature_columns=features,
)

cluster_result = run_dbscan_clustering(
    cluster_data,
    eps=0.8,
    min_samples=6,
)

tracts["cluster"] = cluster_result["labels"]

metrics = evaluate_clustering(
    cluster_data,
    cluster_result["labels"],
)

cluster_summary = summarize_clusters(
    tracts,
    cluster_column="cluster",
    feature_columns=features,
)
```

## What The Helper Returns

The result dictionary contains:

- `model`: fitted DBSCAN model.
- `labels`: cluster labels. Outliers are labeled `-1`.
- `data`: prepared feature table with a cluster column added.
- `cluster_column`: the name of the cluster label column.

## Choosing `eps` And `min_samples`

These parameters matter a lot.

If `eps` is too small:

- Many rows may be labeled `-1`.
- Few clusters may form.

If `eps` is too large:

- Many rows may merge into one large cluster.

If `min_samples` is larger:

- Clusters must be denser.
- More rows may become outliers.

Try several settings and check both metrics and cluster summaries.

```python
for eps in [0.4, 0.6, 0.8, 1.0]:
    result = run_dbscan_clustering(cluster_data, eps=eps, min_samples=6)
    metrics = evaluate_clustering(cluster_data, result["labels"])
    print(eps, metrics["n_clusters"], metrics["n_noise"])
```

## How To Interpret Results

Focus on:

- How many clusters were found.
- How many records were labeled `-1`.
- Whether cluster summaries make sense.
- Whether outliers are meaningful for the research question.

The `-1` group is not a normal cluster. It means DBSCAN considered those records noise or outliers.

## Strengths

- Does not require choosing the number of clusters.
- Can identify outliers.
- Can find irregular cluster shapes.
- Useful for exploratory anomaly screening.

## Limitations

- Very sensitive to `eps`.
- Struggles when clusters have different densities.
- Needs scaled features.
- Can be hard to explain to beginners.
- Performance metrics can be tricky when many points are noise.

## Common Mistakes

- Treating label `-1` as a regular cluster.
- Forgetting that DBSCAN distance is based on model features, not map distance unless coordinates are included.
- Using default `eps=0.5` without testing alternatives.
- Including too many irrelevant features.

## Useful Links

- scikit-learn DBSCAN guide: https://scikit-learn.org/stable/modules/clustering.html#dbscan
- scikit-learn `DBSCAN`: https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html
- Google clustering course: https://developers.google.com/machine-learning/clustering

