# Extra Trees

Extra Trees, short for Extremely Randomized Trees, is an ensemble model similar to random forest. It builds many decision trees, but it adds more randomness when choosing splits.

The extra randomness can make the model faster and sometimes more resistant to overfitting.

## When To Use It

Use Extra Trees when:

- You want a strong tree-based model for tabular data.
- Random forest performs well and you want a related comparison.
- You have nonlinear relationships and feature interactions.
- You are using `compare_models` to test a broad set of models.

Transportation examples:

- Compare Extra Trees against random forest for crash-count prediction.
- Test whether Extra Trees improves congestion classification.
- Use it as one candidate model in a model comparison table.

## Main Idea

Like random forest, Extra Trees trains many decision trees and combines their predictions.

The key difference is how splits are selected. Random forest searches for strong split thresholds among candidate features. Extra Trees uses more random split thresholds, then chooses among those random candidates.

This usually reduces variance. It may slightly increase bias, but the combined ensemble can still be very accurate.

## Helper Function

Use:

```python
from helper.ml import compare_models
```

Model type:

```python
model_type="extra_trees"
```

Implementation file:

```text
helper/ml/compare_models.py
```

Important: `extra_trees` is available in the broad `compare_models` helper. It is not one of the model types accepted by `run_regression_model` or `run_classification_model`.

Inside `compare_models`:

- Regression creates scikit-learn `ExtraTreesRegressor`.
- Classification creates scikit-learn `ExtraTreesClassifier`.
- The helper sets `n_estimators=100`.

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
    model_types=["baseline", "random_forest", "extra_trees"],
)

comparison["results"]
extra_trees_model = comparison["models"]["extra_trees"]
```

## Classification Example

```python
comparison = compare_models(
    split_data,
    task_type="classification",
    model_types=["baseline", "random_forest", "extra_trees"],
)

comparison["results"]
extra_trees_model = comparison["models"]["extra_trees"]
```

## How To Interpret Results

Compare Extra Trees to:

- `baseline`, to make sure the model improves over a simple guess.
- `random_forest`, because they are closely related.
- `gradient_boosting` or `hist_gradient_boosting`, because those are strong tree ensembles with a different learning style.

Extra Trees supports feature importance:

```python
from helper.ml import get_feature_importance

importance = get_feature_importance(
    extra_trees_model,
    feature_names=split_data["X_train"].columns,
)
```

## Strengths

- Often strong on tabular data.
- Captures nonlinear patterns and interactions.
- Can be faster than random forest in some settings.
- Provides feature importance.
- Useful in broad model comparison.

## Limitations

- Less interpretable than linear models or a small decision tree.
- More random splits can underfit some datasets.
- Feature importance has the same cautions as other tree importance methods.
- Not exposed by the single-model helper in this repository.

## Common Mistakes

- Trying `run_regression_model(..., model_type="extra_trees")`, which is not supported.
- Assuming Extra Trees is always better than random forest.
- Comparing models without the baseline row.
- Reporting the best model without explaining the practical metric.

## Useful Links

- scikit-learn ensemble guide: https://scikit-learn.org/stable/modules/ensemble.html#forest
- scikit-learn `ExtraTreesRegressor`: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.ExtraTreesRegressor.html
- scikit-learn `ExtraTreesClassifier`: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.ExtraTreesClassifier.html

