# Linear Regression

Linear regression predicts a numeric outcome by fitting a straight-line relationship between input features and the target.

In a simple one-feature example, the model might learn:

```text
predicted crash count = 0.8 + 0.00003 * traffic_volume
```

With many features, the idea is the same. The model gives each feature a weight and adds the weighted features together.

## When To Use It

Use linear regression when:

- The target is numeric.
- You want a simple, interpretable starting model.
- You expect the relationship to be roughly additive.
- You want to compare complex models against a transparent baseline.

Transportation examples:

- Predict average speed from speed limit, volume, and road class.
- Predict crash count from exposure, speed, and intersection characteristics.
- Predict auto commute share from income, density, and transit access.

## Main Idea

Linear regression tries to find coefficients that make predictions close to observed values. A coefficient tells how much the prediction changes when a feature increases by one unit, while other features stay fixed.

Example:

If `bus_stop_count` has a positive coefficient in a commute model, higher bus stop count is associated with a higher predicted outcome. If `distance_to_rail` has a negative coefficient, farther distance is associated with a lower predicted outcome.

Important: association is not the same as causation. A model can find patterns without proving that one variable causes another.

## Helper Function

Use:

```python
from helper.ml import run_regression_model
```

Model type:

```python
model_type="linear_regression"
```

Implementation files:

```text
helper/ml/run_regression_model.py
helper/ml/_ml_helpers.py
```

Inside the helper, `model_type="linear_regression"` creates scikit-learn `LinearRegression`.

## Example

```python
from helper.ml import (
    prepare_ml_data,
    split_train_test,
    run_regression_model,
    evaluate_regression,
    get_feature_importance,
)

features = [
    "aadt",
    "speed_limit",
    "lane_count",
    "bus_stop_count",
    "road_class",
]

ml_data = prepare_ml_data(
    roads,
    feature_columns=features,
    target_column="speed_ratio",
)

split_data = split_train_test(
    ml_data,
    test_size=0.25,
    random_state=42,
)

result = run_regression_model(
    split_data,
    model_type="linear_regression",
)

metrics = evaluate_regression(
    result["y_test"],
    result["predictions"],
)

importance = get_feature_importance(
    result["model"],
    feature_names=split_data["X_train"].columns,
)
```

## What The Helper Returns

`run_regression_model` returns:

- `model`: the fitted `LinearRegression` model.
- `model_type`: the value `"linear_regression"`.
- `predictions`: predicted numeric values for `X_test`, if test features were provided.
- `X_test`: the test feature table.
- `y_test`: the test target values, when a split dictionary was used.

## How To Interpret Results

Use regression metrics first:

- Lower MAE and RMSE mean smaller prediction errors.
- Higher R2 means the model explains more variation in the target.

Then inspect coefficients with `get_feature_importance`. For linear models, the helper reads the model's coefficients and sorts features by absolute size.

If `prepare_ml_data` scaled numeric features, coefficient sizes are easier to compare across numeric inputs. One-hot encoded categories also appear as separate columns, such as `road_class_primary`.

## Strengths

- Easy to understand and explain.
- Fast to train.
- Useful as a first model.
- Coefficients can support interpretation.

## Limitations

- It assumes a mostly linear, additive relationship.
- It can struggle with thresholds and interactions unless those features are created first.
- It can be sensitive when features are strongly correlated.
- It may underfit complex transportation patterns.

## Common Mistakes

- Treating coefficients as causal effects without research design.
- Using linear regression for a categorical target.
- Forgetting to compare against a baseline.
- Over-interpreting coefficients when features are highly correlated.

## Useful Links

- scikit-learn linear models: https://scikit-learn.org/stable/modules/linear_model.html
- scikit-learn `LinearRegression`: https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html
- Google ML Crash Course, linear regression: https://developers.google.com/machine-learning/crash-course/linear-regression

