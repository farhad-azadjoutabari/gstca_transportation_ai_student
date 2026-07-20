# Hierarchical Clustering

Hierarchical clustering builds groups by repeatedly merging similar rows or clusters. The helper uses agglomerative hierarchical clustering, which means it starts with each row as its own cluster and merges upward.

## When To Use It

Use hierarchical clustering when:

- You have a small or medium dataset.
- You want an interpretable grouping approach.
- You want to compare results with K-Means.
- You want clusters formed by a merging process.

Transportation examples:

- Group a smaller set of corridors into similar profiles.
- Cluster intersections in a study area.
- Group tracts based on demographic and access features.

## Main Idea

Agglomerative hierarchical clustering begins with each row alone. Then it repeatedly merges the two closest clusters until only the requested number remains.

The `linkage` parameter controls how distance between clusters is measured:

- `ward`: merges clusters to reduce within-cluster variance. This is the helper default.
- `complete`: uses the farthest pair between clusters.
- `average`: uses average distance between clusters.
- `single`: uses the closest pair between clusters.

## Helper Function

Use:

```python
from helper.ml import run_hierarchical_clustering, evaluate_clustering, summarize_clusters
```

Implementation file:

```text
helper/ml/run_hierarchical_clustering.py
```

Inside the helper, `run_hierarchical_clustering` creates scikit-learn `AgglomerativeClustering`.

## Example

```python
from helper.ml import (
    prepare_ml_data,
    run_hierarchical_clustering,
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

cluster_result = run_hierarchical_clustering(
    cluster_data,
    n_clusters=4,
    linkage="ward",
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

- `model`: fitted agglomerative clustering model.
- `labels`: cluster label for each row.
- `data`: prepared feature table with a cluster column added.
- `cluster_column`: the name of the cluster label column.

## Choosing The Number Of Clusters

Hierarchical clustering still needs `n_clusters`. Try a few values and compare:

- Cluster counts.
- Silhouette score.
- Cluster summaries.
- Whether the groups make planning sense.

```python
for k in [2, 3, 4, 5, 6]:
    result = run_hierarchical_clustering(cluster_data, n_clusters=k)
    metrics = evaluate_clustering(cluster_data, result["labels"])
    print(k, metrics["silhouette_score"])
```

## How To Interpret Results

Use `summarize_clusters` to describe each cluster. The algorithm gives cluster numbers, but the analyst gives clusters meaning.

Good interpretation:

```text
Cluster 0 contains high-density tracts with high employment and many bus stops.
Cluster 1 contains lower-density tracts with lower transit access.
```

Weak interpretation:

```text
Cluster 0 is better than Cluster 1.
```

Cluster numbers are labels, not ranks.

## Strengths

- Conceptually intuitive merging process.
- Useful for smaller datasets.
- Can reveal nested group structure.
- Does not depend on random initialization.

## Limitations

- Can be slower on large datasets.
- Still requires choosing `n_clusters`.
- Sensitive to feature scaling.
- Once clusters are merged, the algorithm does not undo earlier merges.

## Common Mistakes

- Treating cluster numbers as ordered values.
- Using too many noisy features.
- Forgetting to scale features.
- Assuming hierarchical clustering is always more interpretable than K-Means.

## Useful Links

- scikit-learn hierarchical clustering guide: https://scikit-learn.org/stable/modules/clustering.html#hierarchical-clustering
- scikit-learn `AgglomerativeClustering`: https://scikit-learn.org/stable/modules/generated/sklearn.cluster.AgglomerativeClustering.html
- Google clustering course: https://developers.google.com/machine-learning/clustering

