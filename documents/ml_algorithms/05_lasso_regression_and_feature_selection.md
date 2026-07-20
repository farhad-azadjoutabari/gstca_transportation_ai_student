# Lasso Regression and Feature Selection

Lasso regression is a linear regression model with a penalty that can shrink some coefficients all the way to zero. Because zero coefficients effectively remove features from the model, lasso can be used as a simple feature-selection method.

## When To Use It

Use lasso regression when:

- The target is numeric.
- You want a simpler linear model.
- You have many candidate features.
- You suspect only some features are useful.
- You want a first pass at feature selection.

Transportation examples:

- Start with many tract-level demographic, land-use, and access variables, then identify a smaller set related to mode share.
- Start with many road characteristics, then identify which ones are most related to speed ratio.
- Screen many intersection features before deeper safety analysis.

## Main Idea

Lasso adds an L1 regularization penalty to linear regression. This penalty pushes coefficients toward zero. Unlike ridge regression, lasso can make some coefficients exactly zero.

The `alpha` parameter controls how strong the penalty is:

- Small `alpha`: keeps more features.
- Large `alpha`: removes more features by setting coefficients to zero.

This is why lasso is connected to feature selection.

## Helper Function

Use:

```python
from helper.ml import run_regression_model, get_feature_importance
```

Model type:

```python
model_type="lasso"
```

Implementation files:

```text
helper/ml/run_regression_model.py
helper/ml/_ml_helpers.py
helper/ml/get_feature_importance.py
```

Inside the helper, `model_type="lasso"` creates scikit-learn `Lasso`.

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
    "rail_station_count",
    "park_acres",
    "land_use_mix",
]

ml_data = prepare_ml_data(
    tracts,
    feature_columns=features,
    target_column="transit_commute_share",
)

split_data = split_train_test(ml_data, test_size=0.25, random_state=42)

result = run_regression_model(
    split_data,
    model_type="lasso",
    alpha=0.01,
    max_iter=10000,
)

metrics = evaluate_regression(result["y_test"], result["predictions"])

importance = get_feature_importance(
    result["model"],
    feature_names=split_data["X_train"].columns,
)
```

## Reading Lasso Feature Selection

After fitting lasso, inspect the coefficient table:

```python
importance.loc[importance["coefficient"] != 0]
```

Features with nonzero coefficients were kept by the model. Features with zero coefficients were not used in the final linear equation.

This does not prove the kept features are causal. It only says they helped this lasso model predict the target under the selected `alpha`.

## Choosing `alpha`

Try several values:

```python
rows = []

for alpha in [0.001, 0.01, 0.1, 1.0]:
    result = run_regression_model(
        split_data,
        model_type="lasso",
        alpha=alpha,
        max_iter=10000,
    )
    metrics = evaluate_regression(result["y_test"], result["predictions"])
    nonzero = (result["model"].coef_ != 0).sum()
    rows.append({"alpha": alpha, "features_kept": nonzero, **metrics})
```

Choose an `alpha` that balances prediction quality and simplicity.

## Strengths

- Can produce simpler models.
- Helpful when there are many possible features.
- Coefficients are interpretable.
- Can reduce noise by removing weak features.

## Limitations

- If two features are highly correlated, lasso may keep one and drop the other in an unstable way.
- It assumes mostly linear relationships.
- The selected features depend on `alpha`.
- It can perform poorly if the true pattern needs many small feature effects.

## Common Mistakes

- Treating dropped features as unimportant forever.
- Selecting `alpha` based only on which feature list looks good.
- Forgetting to scale numeric features. `prepare_ml_data` scales by default, which helps lasso behave properly.
- Using lasso feature selection as a substitute for domain knowledge.

## Useful Links

- scikit-learn lasso documentation: https://scikit-learn.org/stable/modules/linear_model.html#lasso
- scikit-learn `Lasso`: https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Lasso.html
- scikit-learn feature selection guide: https://scikit-learn.org/stable/modules/feature_selection.html
- Google ML Crash Course, overfitting and regularization: https://developers.google.com/machine-learning/crash-course/overfitting

