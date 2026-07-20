# Feature Importance and Model Explanation

Feature importance helps answer: "Which input variables did the model rely on most?"

Model explanation is broader. It includes:

- How well the model performed.
- Which features mattered.
- Where the model made the largest errors.
- Which records were misclassified.

This is especially important in transportation analysis because a model score alone is not enough. Students should connect model behavior back to planning meaning.

## When To Use It

Use feature importance and model explanation after training a supervised model.

Good questions:

- Which features were most important for predicting crash count?
- Which variables helped classify high-crash intersections?
- Where did the model make its largest speed-ratio errors?
- Does the model rely on meaningful transportation features or suspicious proxy variables?

## Helper Functions

Use:

```python
from helper.ml import get_feature_importance, explain_model_results, predict_with_model
```

Implementation files:

```text
helper/ml/get_feature_importance.py
helper/ml/explain_model_results.py
helper/ml/predict_with_model.py
```

## `get_feature_importance`

`get_feature_importance` works with fitted models that provide:

- `feature_importances_`, used by many tree models.
- `coef_`, used by linear and logistic models.

It returns a sorted table.

Example:

```python
from helper.ml import get_feature_importance

importance = get_feature_importance(
    result["model"],
    feature_names=split_data["X_train"].columns,
    top_n=15,
)

importance
```

For tree models, the output has:

- `feature`
- `importance`

For linear or logistic models, the output has:

- `feature`
- `coefficient`
- `importance`, which is the absolute coefficient size.

## `explain_model_results`

`explain_model_results` creates a bundle of outputs for a fitted model.

Example:

```python
from helper.ml import explain_model_results

explanation = explain_model_results(
    result["model"],
    result["X_test"],
    result["y_test"],
    task_type="regression",
    top_n=15,
    include_permutation=True,
)

explanation.keys()
```

The dictionary can include:

- `task_type`: regression or classification.
- `predictions`: model predictions.
- `metrics`: regression or classification metrics.
- `feature_importance`: built-in importance or coefficient table, when available.
- `permutation_importance`: model-agnostic importance table, when `y` is provided.
- `error_table`: largest regression errors or misclassified classification rows.

## Permutation Importance

Permutation importance asks:

```text
What happens to model performance if one feature is randomly shuffled?
```

If shuffling a feature makes performance much worse, the model depended on that feature.

This is useful because it can work with many model types, including models that do not have built-in feature importance.

In the helper:

```python
explanation = explain_model_results(
    model,
    X_test,
    y_test,
    task_type="classification",
    include_permutation=True,
    n_repeats=5,
)

explanation["permutation_importance"]
```

## `predict_with_model`

After a model is trained, use it to predict new rows:

```python
from helper.ml import predict_with_model

predicted = predict_with_model(
    result["model"],
    ml_data["X"],
    output_column="predicted_crash_count",
)
```

For classification models with `predict_proba`, the helper can add probability columns:

```python
predicted = predict_with_model(
    result["model"],
    ml_data["X"],
    output_column="predicted_risk",
    include_probabilities=True,
)
```

## Example Full Explanation Workflow

```python
from helper.ml import (
    prepare_ml_data,
    split_train_test,
    run_regression_model,
    explain_model_results,
)

features = ["aadt", "speed_limit", "lane_count", "truck_share", "road_class"]

ml_data = prepare_ml_data(
    roads,
    feature_columns=features,
    target_column="speed_ratio",
)

split_data = split_train_test(ml_data, test_size=0.25, random_state=42)

result = run_regression_model(
    split_data,
    model_type="random_forest",
)

explanation = explain_model_results(
    result["model"],
    result["X_test"],
    result["y_test"],
    task_type="regression",
)

explanation["metrics"]
explanation["feature_importance"]
explanation["permutation_importance"]
explanation["error_table"]
```

## How To Write About Feature Importance

Careful wording:

```text
In this fitted random forest, AADT and speed limit had the highest permutation
importance on the test data. This means the model relied on those variables
for prediction. It does not prove that changing AADT or speed limit would
cause the outcome to change by the same amount.
```

Avoid:

```text
AADT caused crashes because it was the most important feature.
```

Feature importance is about model reliance, not automatic causality.

## Common Mistakes

- Explaining a model before checking whether it predicts well.
- Treating feature importance as causal evidence.
- Comparing feature importance values across different models without caution.
- Forgetting that one-hot encoded categories appear as separate dummy features.
- Ignoring correlated features. When features are strongly correlated, importance may be split or unstable.
- Using prediction on new data without applying the same preprocessing. In this project, use the prepared `X` table from `prepare_ml_data`.

## Useful Links

- scikit-learn permutation importance: https://scikit-learn.org/stable/modules/permutation_importance.html
- scikit-learn inspection guide: https://scikit-learn.org/stable/inspection.html
- scikit-learn model evaluation guide: https://scikit-learn.org/stable/modules/model_evaluation.html
- Google ML Crash Course, datasets and generalization: https://developers.google.com/machine-learning/crash-course/overfitting
