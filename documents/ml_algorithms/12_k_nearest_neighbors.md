# K-Nearest Neighbors

K-Nearest Neighbors, often called KNN, predicts a class by looking at the most similar training rows.

For classification, the model asks:

```text
Which training examples are closest to this new row, and what classes do they have?
```

Then it predicts the most common class among the nearest neighbors.

## When To Use It

Use KNN when:

- The target is a category.
- Similar records should have similar labels.
- You want an intuitive distance-based model.
- The dataset is not extremely large.

Transportation examples:

- Classify a road segment by comparing it with similar roads.
- Classify a tract by comparing it with similar tracts.
- Identify whether an intersection is high risk based on nearby examples in feature space.

## Main Idea

KNN does not learn a formula like linear regression or a set of tree splits. It stores the training examples. For each new row, it measures distance to training rows and uses the nearest ones to vote.

The value of K controls how many neighbors vote:

- Small K: more sensitive to local patterns and noise.
- Large K: smoother, but may ignore local differences.

Feature scaling is very important because KNN is distance-based. `prepare_ml_data` scales numeric features by default.

## Helper Functions

Use:

```python
from helper.ml import run_classification_model, compare_models
```

Model type:

```python
model_type="knn"
```

Implementation files:

```text
helper/ml/run_classification_model.py
helper/ml/compare_classification_models.py
helper/ml/compare_models.py
helper/ml/_ml_helpers.py
```

Important: in this repository, KNN is exposed as a classification model. The regression helpers do not include KNN regression.

Inside the helper, `model_type="knn"` creates scikit-learn `KNeighborsClassifier`.

## Example

```python
from helper.ml import (
    prepare_ml_data,
    split_train_test,
    run_classification_model,
    evaluate_classification,
)

features = [
    "population_density",
    "employment_density",
    "bus_stop_count",
    "rail_station_count",
    "median_income",
]

ml_data = prepare_ml_data(
    tracts,
    feature_columns=features,
    target_column="low_auto_commute",
)

split_data = split_train_test(
    ml_data,
    test_size=0.25,
    random_state=42,
    stratify="y",
)

result = run_classification_model(
    split_data,
    model_type="knn",
    n_neighbors=7,
)

metrics = evaluate_classification(
    result["y_test"],
    result["predictions"],
    result["probabilities"],
)
```

## Choosing `n_neighbors`

Try several values:

```python
rows = []

for k in [3, 5, 7, 11, 15]:
    result = run_classification_model(
        split_data,
        model_type="knn",
        n_neighbors=k,
    )
    metrics = evaluate_classification(
        result["y_test"],
        result["predictions"],
        result["probabilities"],
    )
    rows.append({"n_neighbors": k, "f1_macro": metrics["f1_macro"]})
```

Choose the value that works best on held-out test data and is reasonable for the problem.

## Strengths

- Easy to understand.
- Works well when similar rows truly have similar labels.
- No strong linearity assumption.
- Can capture local patterns.

## Limitations

- Sensitive to feature scaling.
- Can be slow for large datasets.
- Less interpretable than linear coefficients or a small tree.
- Can struggle with irrelevant features.
- Does not provide built-in feature importance.

## Common Mistakes

- Turning off scaling before KNN.
- Using too many weak or irrelevant features.
- Using KNN on very large datasets without considering speed.
- Assuming geographic closeness is included. KNN uses feature-space distance unless coordinates are included as features.

## Useful Links

- scikit-learn nearest neighbors guide: https://scikit-learn.org/stable/modules/neighbors.html
- scikit-learn `KNeighborsClassifier`: https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html
- Google ML Crash Course, numerical data and scaling: https://developers.google.com/machine-learning/crash-course/numerical-data

