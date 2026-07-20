# Train/Test Split and Evaluation

Supervised learning means the model learns from examples where the correct answer is already known. Regression and classification are supervised learning tasks.

To know whether a supervised model learned a useful pattern, we should test it on data it did not train on. That is why we split the data into two parts:

- Training data: rows used to fit the model.
- Test data: rows held back until evaluation.

This is like studying with practice problems and then taking a quiz with new problems. If the model only works on the rows it already saw, it may be memorizing instead of learning.

## Helper Functions

Use:

```python
from helper.ml import split_train_test, evaluate_regression, evaluate_classification
```

Implementation files:

```text
helper/ml/split_train_test.py
helper/ml/evaluate_regression.py
helper/ml/evaluate_classification.py
```

## Basic Regression Workflow

Regression predicts a number.

```python
from helper.ml import (
    prepare_ml_data,
    split_train_test,
    run_regression_model,
    evaluate_regression,
)

features = ["population", "bus_stop_count", "total_employees", "park_acres"]

ml_data = prepare_ml_data(
    tracts,
    feature_columns=features,
    target_column="crash_count",
)

split_data = split_train_test(
    ml_data,
    test_size=0.2,
    random_state=42,
)

result = run_regression_model(
    split_data,
    model_type="random_forest",
)

metrics = evaluate_regression(
    result["y_test"],
    result["predictions"],
)

metrics
```

## Basic Classification Workflow

Classification predicts a category.

```python
from helper.ml import (
    prepare_ml_data,
    split_train_test,
    run_classification_model,
    evaluate_classification,
)

features = ["population", "bus_stop_count", "total_employees", "park_acres"]

ml_data = prepare_ml_data(
    tracts,
    feature_columns=features,
    target_column="high_crash_risk",
)

split_data = split_train_test(
    ml_data,
    test_size=0.2,
    random_state=42,
    stratify="y",
)

result = run_classification_model(
    split_data,
    model_type="random_forest",
)

metrics = evaluate_classification(
    result["y_test"],
    result["predictions"],
    result["probabilities"],
)

metrics["confusion_matrix"]
```

## What `split_train_test` Does

The helper accepts the dictionary returned by `prepare_ml_data`, then returns:

- `X_train`: prepared feature rows for training.
- `X_test`: prepared feature rows for testing.
- `y_train`: known target values for training.
- `y_test`: known target values for testing.

Important parameters:

- `test_size=0.2`: 20 percent of rows are used for testing.
- `random_state=42`: makes the random split repeatable.
- `stratify="y"`: for classification, keeps class proportions similar in the train and test sets.

## Regression Metrics

`evaluate_regression` returns:

- `mae`: mean absolute error. Average absolute prediction error. Lower is better.
- `mse`: mean squared error. Penalizes large errors more strongly. Lower is better.
- `rmse`: root mean squared error. Similar to MAE but more sensitive to large errors. Lower is better.
- `r2`: share of target variation explained by the model. Higher is better, but it can be negative when the model is poor.

Example interpretation:

If RMSE is 2.1 for a crash-count model, predictions are often off by around 2 crashes, with bigger misses affecting the metric more.

## Classification Metrics

`evaluate_classification` returns:

- `accuracy`: share of test records classified correctly.
- `precision_macro`: average precision across classes.
- `recall_macro`: average recall across classes.
- `f1_macro`: balance of precision and recall across classes.
- `roc_auc`: probability-ranking quality when class probabilities are available.
- `confusion_matrix`: table of actual classes versus predicted classes.
- `classification_report`: per-class precision, recall, F1, and support.

For imbalanced classes, do not rely only on accuracy. A model can get high accuracy by mostly predicting the largest class.

## Common Mistakes

- Evaluating on the training data instead of the test data.
- Forgetting `stratify="y"` for classification with uneven classes.
- Comparing regression and classification metrics as if they mean the same thing.
- Treating one random split as the final truth. A small dataset can give unstable scores.
- Reporting a metric without explaining what it means in the units of the problem.

## Useful Links

- scikit-learn `train_test_split`: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html
- scikit-learn model evaluation guide: https://scikit-learn.org/stable/modules/model_evaluation.html
- Google ML Crash Course, datasets and generalization: https://developers.google.com/machine-learning/crash-course/overfitting
- Google ML Crash Course, classification: https://developers.google.com/machine-learning/crash-course/classification
