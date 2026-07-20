# Unsupervised Learning

Unsupervised learning finds patterns without a target label.

The dataset has features, but no answer column.

## Simple Definition

```text
features only -> model finds patterns
```

The model is not told which rows are correct or incorrect. Instead, it looks for structure.

## Example

Suppose each row is a Census tract.

Features:

- Population density
- Employment density
- Median income
- Bus stop count
- Park acres
- Land use mix

There may be no label. The question might be:

```text
Which tracts are similar to each other?
```

An unsupervised model can group tracts into clusters.

## Common Unsupervised Tasks

Clustering:

```text
Group similar rows.
```

Dimensionality reduction:

```text
Reduce many features into fewer summary features.
```

Anomaly detection:

```text
Find unusual rows that do not look like most others.
```

Association discovery:

```text
Find patterns in items or events that occur together.
```

## Clustering

Clustering creates groups based on similarity.

Examples:

- K-Means clustering
- DBSCAN clustering
- Hierarchical clustering
- Gaussian mixture models

Transportation example:

```text
Group intersections into similar exposure profiles before comparing crash outcomes.
```

## Dimensionality Reduction

Dimensionality reduction simplifies many columns into fewer columns.

Example:

```text
Use PCA to reduce 20 demographic features into 2 components for visualization.
```

This can make patterns easier to plot or explain, but the new components may be more abstract than the original features.

## How To Evaluate Unsupervised Learning

Unsupervised learning is harder to evaluate because there is no known answer.

Common checks:

- Do clusters have clear differences in feature summaries?
- Are clusters stable when settings change?
- Do clusters make domain sense?
- Are outliers meaningful?
- Do reduced dimensions preserve enough information?

Metrics like silhouette score can help, but they should not replace interpretation.

## Strengths

- Useful when labels are unavailable.
- Helps discover patterns.
- Helps summarize complex data.
- Can support exploration before supervised modeling.

## Limitations

- Results can be subjective.
- There may be no single correct answer.
- Clusters can change based on features and scaling.
- Patterns may not have practical meaning.
- It does not directly predict a target unless combined with another task.

## Common Mistakes

- Treating cluster labels as true categories.
- Assuming cluster 3 is greater than cluster 2.
- Including irrelevant features that distort similarity.
- Forgetting to scale numeric features for distance-based methods.
- Presenting unsupervised results without explaining what the groups mean.

## Useful Links

- Google clustering course: https://developers.google.com/machine-learning/clustering
- Google clustering overview: https://developers.google.com/machine-learning/clustering/overview
- scikit-learn clustering guide: https://scikit-learn.org/stable/modules/clustering.html
- scikit-learn decomposition guide: https://scikit-learn.org/stable/modules/decomposition.html

