# K-Means Clustering

K-Means is an unsupervised learning algorithm that groups similar rows into a fixed number of clusters.

Unsupervised means there is no target column. The model is not trying to predict a known answer. It is trying to discover structure in the data.

## When To Use It

Use K-Means when:

- You want to group similar records.
- You already know or want to test the number of groups.
- Features are numeric and scaled.
- Clusters are expected to be roughly compact in feature space.

Transportation examples:

- Group Census tracts into neighborhood types.
- Group road segments by traffic, speed, and truck characteristics.
- Group intersections by exposure and safety context.
- Group employers or development projects by location and nearby access features.

## Main Idea

K-Means starts by placing K cluster centers, called centroids. Then it repeats two steps:

1. Assign each row to the nearest centroid.
2. Move each centroid to the average position of the rows assigned to it.

The algorithm stops when assignments stop changing much.

K is the number of clusters. If `n_clusters=4`, K-Means creates 4 groups.

## Helper Functions

Use:

```python
from helper.ml import (
    find_best_k_for_kmeans,
    run_kmeans_clustering,
    evaluate_clustering,
    summarize_clusters,
)
```

Implementation files:

```text
helper/ml/find_best_k_for_kmeans.py
helper/ml/run_kmeans_clustering.py
helper/ml/evaluate_clustering.py
helper/ml/summarize_clusters.py
```

Inside the helper, `run_kmeans_clustering` creates scikit-learn `KMeans`. The helper sets `n_init=10` by default unless you provide a different value.

## Example

```python
from helper.ml import (
    prepare_ml_data,
    find_best_k_for_kmeans,
    run_kmeans_clustering,
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

k_scores = find_best_k_for_kmeans(
    cluster_data,
    k_values=range(2, 8),
)

cluster_result = run_kmeans_clustering(
    cluster_data,
    n_clusters=4,
    random_state=42,
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

## Choosing K

`find_best_k_for_kmeans` returns:

- `n_clusters`: number of clusters tested.
- `inertia`: within-cluster compactness. Lower is better, but it almost always decreases as K increases.
- `silhouette_score`: how separated clusters are. Higher is usually better.

Use the scores as guidance, not as automatic truth. Also check whether the resulting clusters make planning sense.

## What `run_kmeans_clustering` Returns

The result dictionary contains:

- `model`: fitted K-Means model.
- `labels`: cluster label for each row.
- `data`: prepared feature table with a cluster column added.
- `cluster_column`: the name of the cluster label column.

## How To Interpret Clusters

Clusters are labels, not explanations. A cluster number like `2` does not mean anything by itself.

Use `summarize_clusters` to describe each cluster:

```python
cluster_summary = summarize_clusters(
    tracts,
    cluster_column="cluster",
    feature_columns=features,
)
```

Then name clusters based on their averages:

- High employment, high transit access.
- Low density, high auto commute.
- High crash exposure, high traffic volume.

## Strengths

- Simple and widely used.
- Good for exploratory grouping.
- Fast on many datasets.
- Works well with scaled numeric features.

## Limitations

- You must choose K.
- Sensitive to feature scaling.
- Sensitive to outliers.
- Works best for compact, roughly round clusters.
- Cluster labels can change if data or random seed changes.

## Common Mistakes

- Including ID or geometry columns as features.
- Forgetting to scale numeric features. `prepare_ml_data` scales by default.
- Treating cluster numbers as ranked values.
- Choosing K based only on a metric without checking interpretability.
- Using clustering as if it proved cause and effect.

## Useful Links

- scikit-learn clustering guide: https://scikit-learn.org/stable/modules/clustering.html#k-means
- scikit-learn `KMeans`: https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html
- Google clustering course: https://developers.google.com/machine-learning/clustering

