# Gradient Boosting

Gradient boosting is an ensemble method that builds many small decision trees in sequence. Each new tree tries to correct mistakes made by the previous trees.

Random forest builds many trees independently. Gradient boosting builds trees one after another, so the model gradually improves.

## When To Use It

Use gradient boosting when:

- You want a strong predictive model for tabular data.
- The relationship may be nonlinear.
- You expect feature interactions.
- Random forest is good but you want to test another powerful tree ensemble.

Transportation examples:

- Predict crash counts from intersection exposure and context.
- Predict speed ratio from road and traffic characteristics.
- Classify high-congestion links.
- Classify high-risk intersections.

## Main Idea

Gradient boosting starts with a simple prediction. Then it repeatedly adds small trees. Each tree focuses on the remaining errors.

The model has two important ideas:

- It learns gradually.
- It combines many weak learners into one strong model.

Because boosting can fit complex patterns, it needs careful evaluation on test data.

## Helper Functions

Use:

```python
from helper.ml import run_regression_model, run_classification_model, compare_models
```

Model type:

```python
model_type="gradient_boosting"
```

Implementation files:

```text
helper/ml/run_regression_model.py
helper/ml/run_classification_model.py
helper/ml/compare_models.py
helper/ml/_ml_helpers.py
```

Inside the helpers:

- Regression creates scikit-learn `GradientBoostingRegressor`.
- Classification creates scikit-learn `GradientBoostingClassifier`.

## Regression Example

```python
from helper.ml import (
    prepare_ml_data,
    split_train_test,
    run_regression_model,
    evaluate_regression,
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
    model_type="gradient_boosting",
    n_estimators=150,
    learning_rate=0.05,
    max_depth=3,
)

metrics = evaluate_regression(result["y_test"], result["predictions"])
```

## Classification Example

```python
from helper.ml import run_classification_model, evaluate_classification

result = run_classification_model(
    split_data,
    model_type="gradient_boosting",
    n_estimators=150,
    learning_rate=0.05,
    max_depth=3,
)

metrics = evaluate_classification(
    result["y_test"],
    result["predictions"],
    result["probabilities"],
)
```

## Important Parameters

- `n_estimators`: number of trees.
- `learning_rate`: how much each new tree contributes. Smaller values learn more slowly.
- `max_depth`: maximum depth of each tree. Smaller trees often generalize better.
- `random_state`: makes results reproducible.

## How To Interpret Results

Gradient boosting supports feature importance:

```python
from helper.ml import get_feature_importance

importance = get_feature_importance(
    result["model"],
    feature_names=split_data["X_train"].columns,
)
```

Use `explain_model_results` for metrics, feature importance, permutation importance, predictions, and largest errors:

```python
from helper.ml import explain_model_results

explanation = explain_model_results(
    result["model"],
    result["X_test"],
    result["y_test"],
    task_type="regression",
)
```

## Strengths

- Often very accurate on tabular data.
- Captures nonlinear relationships.
- Captures interactions between features.
- Provides feature importance.
- Works for regression and classification.

## Limitations

- More sensitive to parameter choices than random forest.
- Can overfit if too many trees are used or trees are too deep.
- Less transparent than linear models.
- Training can be slower than simple models.

## Common Mistakes

- Increasing `n_estimators` without checking test performance.
- Using a large `learning_rate` and deep trees together.
- Reporting only accuracy for imbalanced classification.
- Treating feature importance as causal proof.

## Useful Links

- scikit-learn gradient boosting guide: https://scikit-learn.org/stable/modules/ensemble.html#gradient-boosting
- scikit-learn `GradientBoostingRegressor`: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingRegressor.html
- scikit-learn `GradientBoostingClassifier`: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingClassifier.html

