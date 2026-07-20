# Principal Component Analysis

Principal Component Analysis, or PCA, reduces many numeric features into a smaller number of new columns called principal components.

PCA is not a prediction model. It is a dimensionality reduction method. It helps simplify many related variables.

## When To Use It

Use PCA when:

- You have many numeric features.
- Several features are correlated.
- You want to visualize complex data in two dimensions.
- You want simplified inputs for clustering.
- You want to explore broad patterns before modeling.

Transportation examples:

- Reduce many demographic variables into a few neighborhood pattern components.
- Visualize tracts based on land use, access, and income features.
- Create two PCA columns for a scatterplot of clusters.
- Simplify related exposure variables before clustering intersections.

## Main Idea

PCA creates new columns that capture directions of variation in the data.

The first principal component, often called `PC1`, captures the largest amount of variation. The second component, `PC2`, captures the next largest amount while being uncorrelated with `PC1`.

Each component is a weighted combination of the original features. Those weights are called loadings.

## Helper Function

Use:

```python
from helper.ml import run_pca
```

Implementation file:

```text
helper/ml/run_pca.py
```

Inside the helper, `run_pca` creates scikit-learn `PCA`.

## Example

```python
from helper.ml import prepare_ml_data, run_pca, run_kmeans_clustering

features = [
    "population_density",
    "employment_density",
    "median_income",
    "zero_vehicle_share",
    "bus_stop_count",
    "land_use_mix",
]

pca_data = prepare_ml_data(
    tracts,
    feature_columns=features,
)

pca_result = run_pca(
    pca_data,
    n_components=2,
)

tracts["PC1"] = pca_result["data"]["PC1"]
tracts["PC2"] = pca_result["data"]["PC2"]

pca_result["explained_variance_ratio"]
pca_result["loadings"]
```

## What The Helper Returns

`run_pca` returns:

- `model`: fitted PCA model.
- `data`: DataFrame with component columns such as `PC1` and `PC2`.
- `explained_variance_ratio`: share of variation captured by each component.
- `loadings`: table showing how original features contribute to each component.

## Understanding Explained Variance

The explained variance ratio tells how much of the original feature variation is captured by each component.

Example:

```text
PC1 = 0.42
PC2 = 0.21
```

This means the first two components together capture 63 percent of the variation in the prepared features.

Higher is not automatically better. PCA is for simplification, so you decide how much detail is acceptable to lose.

## Understanding Loadings

Loadings show which original features contribute to each component.

Example interpretation:

```text
PC1 has high positive loadings for population density, employment density, and bus stops.
This component may represent an urban intensity pattern.
```

Use domain judgment when naming components. PCA does not name them for you.

## PCA Before Clustering

You can cluster using PCA components:

```python
cluster_result = run_kmeans_clustering(
    pca_result["data"],
    n_clusters=4,
)

tracts["cluster"] = cluster_result["labels"]
```

This can help when many original features are highly correlated. However, clustering on PCA components may be less directly interpretable than clustering on original prepared features.

## Strengths

- Simplifies many related features.
- Useful for visualization.
- Can reduce noise.
- Can help clustering when many features overlap.

## Limitations

- Components are combinations of features, so they can be abstract.
- PCA is linear.
- It is sensitive to feature scaling, so scaling matters.
- It does not use the target column and does not directly predict outcomes.

## Common Mistakes

- Treating PCA as a supervised prediction model.
- Forgetting to scale features. `prepare_ml_data` scales numeric features by default.
- Assuming PC1 is always the most important planning concept.
- Naming components without checking loadings.
- Using PCA components and then forgetting what original features they represent.

## Useful Links

- scikit-learn decomposition and PCA guide: https://scikit-learn.org/stable/modules/decomposition.html#pca
- scikit-learn `PCA`: https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html
- Google clustering course, dimensionality reduction context: https://developers.google.com/machine-learning/clustering

