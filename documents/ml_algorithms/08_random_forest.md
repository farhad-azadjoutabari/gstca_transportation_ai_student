# Random Forest

A random forest is a collection of many decision trees. Each tree sees a slightly different version of the data, and the forest combines their predictions.

For regression, the forest usually averages the tree predictions.

For classification, the forest usually votes across trees or averages class probabilities.

## When To Use It

Use random forest when:

- You want a strong general-purpose model for tabular data.
- The relationship may be nonlinear.
- Features may interact with each other.
- You want feature importance.
- You want a model that is usually more stable than one decision tree.

Transportation examples:

- Predict crash count from exposure, geometry, signals, and context.
- Predict speed ratio from road class, volume, and truck share.
- Classify high-risk intersections.
- Classify low-auto-commute tracts.

## Main Idea

Random forests use two sources of randomness:

- Each tree trains on a random sample of rows.
- Each split considers a random subset of features.

This makes trees different from each other. A single tree may overfit, but averaging many different trees usually improves stability and prediction quality.

## Helper Functions

Use:

```python
from helper.ml import run_regression_model, run_classification_model
```

Model type:

```python
model_type="random_forest"
```

Implementation files:

```text
helper/ml/run_regression_model.py
helper/ml/run_classification_model.py
helper/ml/_ml_helpers.py
```

Inside the helpers:

- Regression creates scikit-learn `RandomForestRegressor`.
- Classification creates scikit-learn `RandomForestClassifier`.
- If `n_estimators` is not provided, the helper sets `n_estimators=100`.

## Regression Example

```python
from helper.ml import (
    prepare_ml_data,
    split_train_test,
    run_regression_model,
    evaluate_regression,
    explain_model_results,
)

features = [
    "aadt",
    "speed_limit",
    "lane_count",
    "truck_share",
    "signal_count",
    "road_class",
]

ml_data = prepare_ml_data(
    roads,
    feature_columns=features,
    target_column="speed_ratio",
)

split_data = split_train_test(ml_data, test_size=0.25, random_state=42)

result = run_regression_model(
    split_data,
    model_type="random_forest",
    n_estimators=300,
    min_samples_leaf=5,
)

metrics = evaluate_regression(result["y_test"], result["predictions"])

explanation = explain_model_results(
    result["model"],
    result["X_test"],
    result["y_test"],
    task_type="regression",
)
```

## Classification Example

```python
from helper.ml import prepare_ml_data, split_train_test, run_classification_model

ml_data = prepare_ml_data(
    intersections,
    feature_columns=features,
    target_column="high_crash_risk",
)

split_data = split_train_test(
    ml_data,
    test_size=0.25,
    random_state=42,
    stratify="y",
)

result = run_classification_model(
    split_data,
    model_type="random_forest",
    n_estimators=300,
    min_samples_leaf=5,
)
```

## Important Parameters

- `n_estimators`: number of trees. More trees usually improve stability but take longer.
- `max_depth`: maximum depth of each tree.
- `min_samples_leaf`: minimum records in a final leaf. Larger values reduce overfitting.
- `random_state`: makes the fitted forest reproducible.

## How To Interpret Results

Random forest models provide `feature_importances_`, so the helper can extract feature importance:

```python
from helper.ml import get_feature_importance

importance = get_feature_importance(
    result["model"],
    feature_names=split_data["X_train"].columns,
    top_n=15,
)
```

For a stronger interpretation, use permutation importance through `explain_model_results`. Permutation importance measures how much model performance drops when a feature is shuffled.

## Strengths

- Strong default model for many tabular datasets.
- Handles nonlinear relationships and interactions.
- More stable than a single decision tree.
- Provides feature importance.
- Works for regression and classification.

## Limitations

- Less transparent than a single decision tree.
- Can still overfit if trees are too deep and leaves are too small.
- Feature importance can be biased toward continuous or high-cardinality features.
- Predictions may not extrapolate well outside the range of training data.

## Common Mistakes

- Reporting feature importance without evaluating model performance first.
- Assuming the top feature causes the outcome.
- Using random forest as the only model without comparing to a baseline.
- Ignoring class imbalance in classification.

## Useful Links

- scikit-learn ensemble guide: https://scikit-learn.org/stable/modules/ensemble.html#forest
- scikit-learn `RandomForestRegressor`: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html
- scikit-learn `RandomForestClassifier`: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html
- scikit-learn permutation importance: https://scikit-learn.org/stable/modules/permutation_importance.html

