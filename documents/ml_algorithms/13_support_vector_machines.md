# Support Vector Machines

Support Vector Machines, or SVMs, are classification models that try to separate classes with the widest possible margin.

For a simple two-class problem, imagine drawing a boundary between high-risk and not-high-risk records. SVM tries to place the boundary so the closest records on each side are as far from the boundary as possible.

## When To Use It

Use SVM when:

- The target is a category.
- You want a strong classifier for a small or medium dataset.
- The boundary between classes may be complex.
- You have scaled numeric features.

Transportation examples:

- Classify high-crash-risk intersections.
- Classify severe-congestion road links.
- Classify low-auto-commute tracts.

## Main Idea

The most important points for an SVM are the records near the class boundary. These are called support vectors. They help define where the boundary should go.

With kernels, SVM can draw nonlinear boundaries. The default scikit-learn `SVC` uses the radial basis function kernel unless changed.

Feature scaling is very important because SVM uses distances and margins. `prepare_ml_data` scales numeric features by default.

## Helper Functions

Use:

```python
from helper.ml import run_classification_model, compare_models
```

Model type:

```python
model_type="svm"
```

Implementation files:

```text
helper/ml/run_classification_model.py
helper/ml/compare_classification_models.py
helper/ml/compare_models.py
helper/ml/_ml_helpers.py
```

Important: in this repository, SVM is exposed as a classification model. The regression helpers do not include SVM regression.

Inside the helper, `model_type="svm"` creates scikit-learn `SVC` and sets `probability=True` by default so class probabilities can be returned.

## Example

```python
from helper.ml import (
    prepare_ml_data,
    split_train_test,
    run_classification_model,
    evaluate_classification,
)

features = [
    "aadt",
    "speed_limit",
    "lane_count",
    "truck_share",
    "signal_count",
]

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

result = run_classification_model(
    split_data,
    model_type="svm",
    C=1.0,
    kernel="rbf",
)

metrics = evaluate_classification(
    result["y_test"],
    result["predictions"],
    result["probabilities"],
)
```

## Important Parameters

- `C`: controls the tradeoff between a wide margin and classifying training examples correctly. Smaller values allow more mistakes; larger values fit training data more tightly.
- `kernel`: shape of the boundary. Common values include `"rbf"` and `"linear"`.
- `gamma`: controls how local the influence of each training point is for RBF kernels.

These can be passed into `run_classification_model` as extra keyword arguments.

## How To Interpret Results

Use classification metrics and the confusion matrix:

```python
metrics["confusion_matrix"]
metrics["classification_report"]
```

SVM does not provide simple built-in feature importance for nonlinear kernels. If you need explanation, use permutation importance through `explain_model_results`:

```python
from helper.ml import explain_model_results

explanation = explain_model_results(
    result["model"],
    result["X_test"],
    result["y_test"],
    task_type="classification",
    include_permutation=True,
)
```

## Strengths

- Strong classifier for many small or medium datasets.
- Can create nonlinear decision boundaries.
- Focuses on difficult boundary cases.
- Works well when features are scaled.

## Limitations

- Can be slower on larger datasets.
- Sensitive to parameter choices.
- Harder to explain than linear models or trees.
- Probability estimates require extra fitting work, which the helper enables with `probability=True`.

## Common Mistakes

- Turning off scaling before SVM.
- Using SVM on a very large dataset without checking runtime.
- Reporting accuracy only for imbalanced classes.
- Expecting simple feature coefficients when using nonlinear kernels.

## Useful Links

- scikit-learn SVM guide: https://scikit-learn.org/stable/modules/svm.html
- scikit-learn `SVC`: https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html
- Google ML Crash Course, classification: https://developers.google.com/machine-learning/crash-course/classification

