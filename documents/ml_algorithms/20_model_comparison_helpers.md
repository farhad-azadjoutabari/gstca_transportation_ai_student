# Model Comparison Helpers

Model comparison means training several models on the same train/test split and comparing their test performance.

This is useful because there is rarely one best algorithm for every dataset. A simple model may be enough, or a more complex model may improve prediction.

## Helper Functions

The repository has three comparison helpers:

```python
from helper.ml import (
    compare_regression_models,
    compare_classification_models,
    compare_models,
)
```

Implementation files:

```text
helper/ml/compare_regression_models.py
helper/ml/compare_classification_models.py
helper/ml/compare_models.py
```

## `compare_regression_models`

Use this for numeric targets when you want the standard challenge-friendly regression set.

Default models:

- `linear_regression`
- `ridge`
- `lasso`
- `decision_tree`
- `random_forest`
- `gradient_boosting`

Example:

```python
from helper.ml import prepare_ml_data, split_train_test, compare_regression_models

features = ["aadt", "speed_limit", "lane_count", "truck_share", "road_class"]

ml_data = prepare_ml_data(
    roads,
    feature_columns=features,
    target_column="speed_ratio",
)

split_data = split_train_test(ml_data, test_size=0.25, random_state=42)

comparison = compare_regression_models(split_data)

comparison["results"]
```

The output dictionary contains:

- `results`: table sorted by RMSE.
- `models`: fitted model for each model type.
- `predictions`: test predictions for each model type.

## `compare_classification_models`

Use this for categorical targets when you want the standard challenge-friendly classification set.

Default models:

- `logistic_regression`
- `decision_tree`
- `random_forest`
- `gradient_boosting`
- `knn`
- `svm`

Example:

```python
from helper.ml import prepare_ml_data, split_train_test, compare_classification_models

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

comparison = compare_classification_models(split_data)

comparison["results"]
```

The output dictionary contains:

- `results`: table sorted by F1 macro.
- `models`: fitted model for each model type.
- `predictions`: test predictions for each model type.
- `probabilities`: class probabilities when available.

## `compare_models`

Use this when you want the broadest comparison. It supports both regression and classification and includes a baseline model.

Regression default models:

- `baseline`
- `linear_regression`
- `ridge`
- `lasso`
- `decision_tree`
- `random_forest`
- `extra_trees`
- `gradient_boosting`
- `hist_gradient_boosting`

Classification default models:

- `baseline`
- `logistic_regression`
- `decision_tree`
- `random_forest`
- `extra_trees`
- `gradient_boosting`
- `hist_gradient_boosting`
- `knn`
- `svm`

Regression example:

```python
comparison = compare_models(
    split_data,
    task_type="regression",
)

comparison["results"]
```

Classification example:

```python
comparison = compare_models(
    split_data,
    task_type="classification",
)

comparison["results"]
```

## Custom Model Lists

You can choose a smaller model list:

```python
comparison = compare_models(
    split_data,
    task_type="classification",
    model_types=[
        "baseline",
        "logistic_regression",
        "random_forest",
        "gradient_boosting",
        "knn",
    ],
)
```

This is helpful when a model is slow or not appropriate for the assignment.

## Understanding The Results Table

For regression:

- The table is sorted by `rmse`, then `mae`.
- Lower `mae`, `mse`, and `rmse` are better.
- Higher `r2` is better.

For classification:

- The table is sorted by `f1_macro`, then `accuracy`.
- Higher `accuracy`, `precision_macro`, `recall_macro`, and `f1_macro` are better.
- `roc_auc` may be `None` when it cannot be calculated.

## Getting The Best Model

```python
results = comparison["results"]
best_model_type = results.iloc[0]["model_type"]
best_model = comparison["models"][best_model_type]
```

Then explain it:

```python
from helper.ml import explain_model_results

explanation = explain_model_results(
    best_model,
    split_data["X_test"],
    split_data["y_test"],
    task_type=comparison["task_type"],
)
```

## Errors Table

`compare_models` has `continue_on_error=True` by default. If one model fails, the helper records the failure instead of stopping the whole comparison.

Check:

```python
comparison["errors"]
```

If this table is not empty, report which model failed and why.

## How To Choose A Final Model

The best metric is not the only consideration. Also ask:

- Does it beat the baseline?
- Is the improvement meaningful in real units?
- Is the model explainable enough for the audience?
- Does it perform reasonably for important classes?
- Does it rely on sensible features?
- Is it stable enough for the dataset size?

For a report, it is often good to show the comparison table, select the best model by a clear metric, then explain that model.

## Common Mistakes

- Selecting a model only because it sounds advanced.
- Ignoring the baseline row.
- Comparing models trained on different splits.
- Reporting only one metric.
- Forgetting to inspect `comparison["errors"]`.
- Treating model comparison as proof that the outcome is fully predictable.

## Useful Links

- scikit-learn model evaluation guide: https://scikit-learn.org/stable/modules/model_evaluation.html
- scikit-learn choosing the right estimator: https://scikit-learn.org/stable/machine_learning_map.html
- scikit-learn ensemble guide: https://scikit-learn.org/stable/modules/ensemble.html
- Google ML Crash Course: https://developers.google.com/machine-learning/crash-course/

