# Ridge Regression

Ridge regression is a linear regression model with a penalty that discourages very large coefficients. It still predicts a numeric outcome, but it tries to make the model less sensitive to noisy or highly correlated features.

Think of ridge as linear regression with a stabilizer.

## When To Use It

Use ridge regression when:

- The target is numeric.
- You want a linear model.
- Some features are correlated with each other.
- Ordinary linear regression looks unstable or overfits.
- You have many features and want a model that generalizes better.

Transportation examples:

- Predict crash count using several related exposure variables.
- Predict speed ratio using volume, truck volume, lane count, and road class.
- Predict mode share using many demographic variables that are correlated.

## Main Idea

Ordinary linear regression chooses coefficients that minimize prediction error. Ridge regression minimizes prediction error plus a penalty for large coefficients.

The penalty is called L2 regularization.

The `alpha` parameter controls the strength of the penalty:

- Small `alpha`: behaves more like ordinary linear regression.
- Large `alpha`: shrinks coefficients more strongly.

Ridge usually does not set coefficients exactly to zero. It shrinks them toward zero.

## Helper Function

Use:

```python
from helper.ml import run_regression_model
```

Model type:

```python
model_type="ridge"
```

Implementation files:

```text
helper/ml/run_regression_model.py
helper/ml/_ml_helpers.py
```

Inside the helper, `model_type="ridge"` creates scikit-learn `Ridge`.

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
    "population",
    "employment_density",
    "median_income",
    "zero_vehicle_share",
    "bus_stop_count",
]

ml_data = prepare_ml_data(
    tracts,
    feature_columns=features,
    target_column="auto_commute_share",
)

split_data = split_train_test(ml_data, test_size=0.25, random_state=42)

result = run_regression_model(
    split_data,
    model_type="ridge",
    alpha=1.0,
)

metrics = evaluate_regression(result["y_test"], result["predictions"])

importance = get_feature_importance(
    result["model"],
    feature_names=split_data["X_train"].columns,
)
```

Because `run_regression_model` passes extra keyword arguments to scikit-learn, `alpha=1.0` goes directly to `Ridge`.

## Choosing `alpha`

Try a few values and compare test RMSE:

```python
rows = []

for alpha in [0.01, 0.1, 1.0, 10.0, 100.0]:
    result = run_regression_model(split_data, model_type="ridge", alpha=alpha)
    metrics = evaluate_regression(result["y_test"], result["predictions"])
    rows.append({"alpha": alpha, **metrics})
```

A good `alpha` is one that improves test performance, not just training performance.

## How To Interpret Results

Ridge coefficients are interpreted like linear regression coefficients, but they are intentionally shrunk. If numeric features were scaled by `prepare_ml_data`, coefficient sizes are more comparable.

Use:

```python
importance = get_feature_importance(
    result["model"],
    feature_names=split_data["X_train"].columns,
)
```

The helper reports coefficient magnitude as importance.

## Strengths

- More stable than ordinary linear regression when features are correlated.
- Still interpretable.
- Often a strong simple model for tabular data.
- Useful when there are many related predictors.

## Limitations

- Still assumes mostly linear relationships.
- Does not automatically select a small set of features.
- The best `alpha` depends on the data.
- Coefficients can still be hard to explain when inputs are highly correlated.

## Common Mistakes

- Using ridge but never comparing it to linear regression or lasso.
- Assuming smaller coefficients mean unimportant variables in an absolute sense.
- Forgetting that regularization strength should be evaluated on test data.
- Using an extremely large `alpha` that shrinks the model too much.

## Useful Links

- scikit-learn linear models: https://scikit-learn.org/stable/modules/linear_model.html#ridge-regression-and-classification
- scikit-learn `Ridge`: https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html
- Google ML Crash Course, overfitting and regularization: https://developers.google.com/machine-learning/crash-course/overfitting

