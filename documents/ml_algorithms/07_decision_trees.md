# Decision Trees

A decision tree predicts by asking a sequence of yes/no questions about the features.

Example:

```text
Is AADT greater than 30,000?
If yes, is speed limit greater than 40?
If no, is there a signal?
```

At the end of the path, the tree gives a prediction.

Decision trees can be used for both regression and classification.

## When To Use It

Use decision trees when:

- You want an easy-to-explain model.
- You expect thresholds to matter.
- You expect feature interactions.
- You want a model that can handle nonlinear patterns.

Transportation examples:

- Predict crash count from traffic volume, speed, and control type.
- Classify roads as congested or not congested.
- Identify combinations of tract characteristics associated with low auto commute share.

## Main Idea

A decision tree repeatedly splits the data into smaller groups. Each split is chosen to make the target values more similar inside the resulting groups.

For regression, leaves predict a number, often the average target value for training rows in that leaf.

For classification, leaves predict a class, often based on the most common class in that leaf. The model can also estimate class probabilities from the class mix in a leaf.

## Helper Functions

Use:

```python
from helper.ml import run_regression_model, run_classification_model
```

Model type:

```python
model_type="decision_tree"
```

Implementation files:

```text
helper/ml/run_regression_model.py
helper/ml/run_classification_model.py
helper/ml/_ml_helpers.py
```

Inside the helpers:

- Regression creates scikit-learn `DecisionTreeRegressor`.
- Classification creates scikit-learn `DecisionTreeClassifier`.

## Regression Example

```python
from helper.ml import prepare_ml_data, split_train_test, run_regression_model

features = ["aadt", "speed_limit", "lane_count", "truck_share", "road_class"]

ml_data = prepare_ml_data(
    roads,
    feature_columns=features,
    target_column="speed_ratio",
)

split_data = split_train_test(ml_data, test_size=0.25, random_state=42)

result = run_regression_model(
    split_data,
    model_type="decision_tree",
    max_depth=4,
    min_samples_leaf=10,
)
```

## Classification Example

```python
from helper.ml import prepare_ml_data, split_train_test, run_classification_model

features = ["aadt", "speed_limit", "lane_count", "truck_share", "road_class"]

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
    model_type="decision_tree",
    max_depth=4,
    min_samples_leaf=10,
)
```

## Important Parameters

- `max_depth`: maximum number of split levels. Smaller values make simpler trees.
- `min_samples_leaf`: minimum records allowed in a final leaf. Larger values reduce overfitting.
- `random_state`: makes random choices reproducible.

Extra parameters are passed from the helper into scikit-learn through `**model_kwargs`.

## How To Interpret Results

Decision trees are often understandable because their logic is based on splits. In this helper package, use:

```python
from helper.ml import get_feature_importance

importance = get_feature_importance(
    result["model"],
    feature_names=split_data["X_train"].columns,
)
```

Tree feature importance shows which features helped reduce error or impurity across the tree. It is useful, but it can be biased toward features with many possible split points.

## Strengths

- Handles nonlinear patterns.
- Captures interactions between features.
- Easy to explain at a high level.
- Works for regression and classification.
- Does not require feature scaling, although `prepare_ml_data` still prepares the table consistently.

## Limitations

- A single tree can overfit badly.
- Small data changes can produce a different tree.
- Predictions are step-like, not smooth.
- Random forests and boosting often predict better.

## Common Mistakes

- Letting the tree grow too deep.
- Reporting a tree model without testing it on held-out data.
- Assuming feature importance proves causality.
- Using a single decision tree when a more stable ensemble is needed.

## Useful Links

- scikit-learn decision tree guide: https://scikit-learn.org/stable/modules/tree.html
- scikit-learn `DecisionTreeRegressor`: https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeRegressor.html
- scikit-learn `DecisionTreeClassifier`: https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html

