# Gaussian Mixture Models

A Gaussian Mixture Model, or GMM, is a clustering model that treats the data as a mixture of several bell-shaped groups. Unlike K-Means, it can give each row a probability of belonging to each cluster.

This is why GMM is often called a soft clustering method.

## When To Use It

Use Gaussian Mixture Models when:

- You want clusters but also want membership probabilities.
- A row may partly belong to more than one group.
- You want to compare soft clustering with K-Means.
- Cluster shapes may be oval rather than round.

Transportation examples:

- Assign tracts to neighborhood profile groups with uncertainty.
- Group road segments where some segments are between typical profiles.
- Cluster intersections and identify records with ambiguous cluster membership.

## Main Idea

GMM assumes the data came from several Gaussian distributions. Each distribution is a component. The model estimates:

- Where each component is centered.
- The shape and spread of each component.
- The probability that each row belongs to each component.

The final cluster label is the most likely component for that row.

## Helper Function

Use:

```python
from helper.ml import run_gaussian_mixture_clustering, evaluate_clustering, summarize_clusters
```

Implementation file:

```text
helper/ml/run_gaussian_mixture_clustering.py
```

Inside the helper, `run_gaussian_mixture_clustering` creates scikit-learn `GaussianMixture`.

## Example

```python
from helper.ml import (
    prepare_ml_data,
    run_gaussian_mixture_clustering,
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

cluster_result = run_gaussian_mixture_clustering(
    cluster_data,
    n_components=4,
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

## What The Helper Returns

The result dictionary contains:

- `model`: fitted Gaussian Mixture model.
- `labels`: most likely cluster/component for each row.
- `probabilities`: probability of each row belonging to each component.
- `data`: prepared feature table with a cluster column added.
- `cluster_column`: the name of the cluster label column.

## Using Probabilities

The `probabilities` array has one row per record and one column per component.

```python
cluster_result["probabilities"][:5]
```

A row with probabilities like this:

```text
[0.92, 0.03, 0.04, 0.01]
```

is strongly assigned to component 0.

A row like this:

```text
[0.38, 0.34, 0.25, 0.03]
```

is more ambiguous. It may sit between several cluster profiles.

## Choosing `n_components`

`n_components` is similar to number of clusters. Try several values and inspect:

- Cluster metrics.
- Cluster summaries.
- Probability patterns.
- Whether clusters make planning sense.

## Strengths

- Provides soft cluster membership probabilities.
- Can model oval cluster shapes.
- Useful for identifying ambiguous records.
- Good comparison to K-Means.

## Limitations

- Requires choosing `n_components`.
- Assumes Gaussian-like components.
- Sensitive to scaling and outliers.
- Can be harder to explain than K-Means.

## Common Mistakes

- Treating the highest-probability cluster as certain when probabilities are close.
- Choosing too many components and over-interpreting small groups.
- Forgetting that GMM clusters are patterns in features, not causal categories.
- Comparing probability values across very different model setups as if they are identical.

## Useful Links

- scikit-learn Gaussian mixture guide: https://scikit-learn.org/stable/modules/mixture.html
- scikit-learn `GaussianMixture`: https://scikit-learn.org/stable/modules/generated/sklearn.mixture.GaussianMixture.html
- Google clustering course: https://developers.google.com/machine-learning/clustering

