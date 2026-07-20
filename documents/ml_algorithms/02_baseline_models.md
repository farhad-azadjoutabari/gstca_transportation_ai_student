# Baseline Models

A baseline model is a simple model used as a reference point. It answers the question: "Does our real model do better than a very simple guess?"

Baselines are important because an impressive-looking model score may not actually be impressive. For example, if 90 percent of road segments are not high-crash segments, a classifier that always predicts "not high crash" could be 90 percent accurate while being useless for safety screening.

## What The Baseline Does

In this project's broad comparison helper:

- Regression baseline predicts the training-set mean for every test row.
- Classification baseline predicts the most frequent class for every test row.

These are intentionally simple. The goal is not to win. The goal is to set a minimum standard that other models should beat.

## Helper Function

Use:

```python
from helper.ml import compare_models
```

Implementation file:

```text
helper/ml/compare_models.py
```

Inside the helper:

- Regression baseline uses scikit-learn `DummyRegressor(strategy="mean")`.
- Classification baseline uses scikit-learn `DummyClassifier(strategy="most_frequent")`.

The smaller helpers `compare_regression_models` and `compare_classification_models` do not include baselines by default. Use `compare_models` when you want baseline comparison.

## Regression Example

```python
from helper.ml import prepare_ml_data, split_train_test, compare_models

features = ["aadt", "speed_limit", "lane_count", "truck_share"]

ml_data = prepare_ml_data(
    roads,
    feature_columns=features,
    target_column="speed_ratio",
)

split_data = split_train_test(ml_data, test_size=0.25, random_state=42)

comparison = compare_models(
    split_data,
    task_type="regression",
)

comparison["results"]
```

Look for the `baseline` row. A useful regression model should usually have lower MAE and RMSE than the baseline.

## Classification Example

```python
from helper.ml import prepare_ml_data, split_train_test, compare_models

features = ["aadt", "speed_limit", "lane_count", "truck_share"]

ml_data = prepare_ml_data(
    roads,
    feature_columns=features,
    target_column="high_congestion",
)

split_data = split_train_test(
    ml_data,
    test_size=0.25,
    random_state=42,
    stratify="y",
)

comparison = compare_models(
    split_data,
    task_type="classification",
)

comparison["results"]
```

Look for the `baseline` row. A useful classifier should usually improve F1, recall, or the metric most relevant to the planning question.

## How To Explain It

Good wording for a report:

```text
The baseline regression model predicts the average training value for every test row.
The best model improves RMSE from 0.19 to 0.12 speed-ratio units, so it performs
better than a simple average-only guess.
```

For classification:

```text
The baseline classifier always predicts the most common class. Because the high-risk
class is less common, F1 is more informative than accuracy.
```

## Common Mistakes

- Skipping the baseline and assuming a complex model is automatically useful.
- Using accuracy alone for imbalanced classification.
- Forgetting that a baseline can be hard to beat when the dataset is noisy or the features are weak.
- Treating a small improvement as meaningful without considering whether the improvement matters in real planning units.

## Useful Links

- scikit-learn dummy estimators: https://scikit-learn.org/stable/modules/model_evaluation.html#dummy-estimators
- scikit-learn `DummyRegressor`: https://scikit-learn.org/stable/modules/generated/sklearn.dummy.DummyRegressor.html
- scikit-learn `DummyClassifier`: https://scikit-learn.org/stable/modules/generated/sklearn.dummy.DummyClassifier.html
- Google ML Crash Course, datasets and generalization: https://developers.google.com/machine-learning/crash-course/overfitting
