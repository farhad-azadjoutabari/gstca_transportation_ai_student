# Histogram Gradient Boosting

Histogram Gradient Boosting is a faster, newer gradient-boosted tree method in scikit-learn. Like regular gradient boosting, it builds trees one after another. The "histogram" part means numeric features are grouped into bins to speed up training.

## When To Use It

Use Histogram Gradient Boosting when:

- You want a strong boosted-tree model.
- The dataset is medium or large.
- `compare_models` includes it as one candidate.
- You want to compare it with random forest, Extra Trees, and regular gradient boosting.

Transportation examples:

- Compare models for crash-count prediction across many road segments.
- Predict speed ratio on many links.
- Classify high-congestion or high-risk locations.

## Main Idea

Boosting learns in stages. Each tree tries to improve the current model. Histogram Gradient Boosting speeds this up by binning feature values before finding splits.

It can be a strong model, but it is less transparent than linear regression or a small tree.

## Helper Function

Use:

```python
from helper.ml import compare_models
```

Model type:

```python
model_type="hist_gradient_boosting"
```

Implementation file:

```text
helper/ml/compare_models.py
```

Important: `hist_gradient_boosting` is available in `compare_models`. It is not one of the model types accepted by `run_regression_model` or `run_classification_model`.

Inside `compare_models`:

- Regression creates scikit-learn `HistGradientBoostingRegressor`.
- Classification creates scikit-learn `HistGradientBoostingClassifier`.

## Regression Example

```python
from helper.ml import prepare_ml_data, split_train_test, compare_models

features = ["aadt", "speed_limit", "lane_count", "truck_share", "road_class"]

ml_data = prepare_ml_data(
    roads,
    feature_columns=features,
    target_column="speed_ratio",
)

split_data = split_train_test(ml_data, test_size=0.25, random_state=42)

comparison = compare_models(
    split_data,
    task_type="regression",
    model_types=[
        "baseline",
        "random_forest",
        "gradient_boosting",
        "hist_gradient_boosting",
    ],
)

comparison["results"]
hist_model = comparison["models"]["hist_gradient_boosting"]
```

## Classification Example

```python
comparison = compare_models(
    split_data,
    task_type="classification",
    model_types=[
        "baseline",
        "random_forest",
        "gradient_boosting",
        "hist_gradient_boosting",
    ],
)

comparison["results"]
hist_model = comparison["models"]["hist_gradient_boosting"]
```

## How To Interpret Results

In `compare_models`, regression results are sorted by RMSE and MAE. Classification results are sorted by F1 and accuracy.

If Histogram Gradient Boosting is best, explain it in terms of the metric:

```text
Histogram Gradient Boosting had the lowest RMSE, so it made the smallest
typical crash-count errors on the held-out intersections.
```

Some histogram gradient boosting estimators may not expose the same built-in feature importance interface as regular tree ensembles. Use permutation importance through `explain_model_results`:

```python
from helper.ml import explain_model_results

explanation = explain_model_results(
    hist_model,
    split_data["X_test"],
    split_data["y_test"],
    task_type="regression",
    include_permutation=True,
)

explanation["permutation_importance"]
```

## Strengths

- Strong predictive model for tabular data.
- Often faster than traditional gradient boosting on larger datasets.
- Handles nonlinear relationships and interactions.
- Available in broad model comparisons.

## Limitations

- Less interpretable than linear models.
- Not exposed by the single-model helper in this repository.
- Parameter tuning can matter.
- Built-in feature importance may not be available, so permutation importance is often better.

## Common Mistakes

- Trying `run_regression_model(..., model_type="hist_gradient_boosting")`, which is not supported.
- Assuming the most complex model is best without checking the baseline.
- Ignoring failed models listed in `comparison["errors"]`.
- Using the model for explanation without first checking test performance.

## Useful Links

- scikit-learn histogram gradient boosting guide: https://scikit-learn.org/stable/modules/ensemble.html#histogram-based-gradient-boosting
- scikit-learn `HistGradientBoostingRegressor`: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.HistGradientBoostingRegressor.html
- scikit-learn `HistGradientBoostingClassifier`: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.HistGradientBoostingClassifier.html

