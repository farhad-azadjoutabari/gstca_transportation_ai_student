# Logistic Regression

Logistic regression is a classification model. Despite the word "regression" in its name, it is usually used to predict categories, especially yes/no outcomes.

It predicts the probability that a row belongs to a class.

Example question:

```text
What is the probability that this intersection is high crash risk?
```

## When To Use It

Use logistic regression when:

- The target is a class or category.
- You want an interpretable classifier.
- You want predicted probabilities.
- You need a simple model before trying trees or boosting.

Transportation examples:

- Predict whether an intersection is high crash risk.
- Predict whether a road segment is severely congested.
- Predict whether a tract is in the lowest auto-commute-share group.
- Predict whether a location should be marked as priority or not priority.

## Main Idea

Linear regression predicts a number directly. Logistic regression first builds a linear score, then converts that score into a probability between 0 and 1.

For binary classification:

- Probability near 0 means the model thinks the class is unlikely.
- Probability near 1 means the model thinks the class is likely.
- A threshold, often 0.5, turns the probability into a class prediction.

The helper returns both predicted classes and probabilities when the model supports them.

## Helper Function

Use:

```python
from helper.ml import run_classification_model
```

Model type:

```python
model_type="logistic_regression"
```

Implementation files:

```text
helper/ml/run_classification_model.py
helper/ml/_ml_helpers.py
```

Inside the helper, `model_type="logistic_regression"` creates scikit-learn `LogisticRegression` with `max_iter=1000` by default.

## Example

```python
from helper.ml import (
    prepare_ml_data,
    split_train_test,
    run_classification_model,
    evaluate_classification,
    get_feature_importance,
)

features = [
    "aadt",
    "speed_limit",
    "lane_count",
    "signal_present",
    "crosswalk_count",
]

ml_data = prepare_ml_data(
    intersections,
    feature_columns=features,
    target_column="high_crash_risk",
)

split_data = split_train_test(
    ml_data,
    test_size=0.25,
    random_state=42,
    stratify="y",
)

result = run_classification_model(
    split_data,
    model_type="logistic_regression",
)

metrics = evaluate_classification(
    result["y_test"],
    result["predictions"],
    result["probabilities"],
)

importance = get_feature_importance(
    result["model"],
    feature_names=split_data["X_train"].columns,
)
```

## What The Helper Returns

`run_classification_model` returns:

- `model`: the fitted logistic regression model.
- `model_type`: the value `"logistic_regression"`.
- `predictions`: predicted class labels for `X_test`.
- `probabilities`: predicted class probabilities for `X_test`.
- `X_test`: the test feature table.
- `y_test`: the test target values, when a split dictionary was used.

## How To Interpret Results

Use classification metrics:

- Accuracy: overall share correct.
- Precision: when the model predicts a class, how often it is right.
- Recall: out of the real class members, how many the model finds.
- F1: balance between precision and recall.
- Confusion matrix: where the model confuses classes.

Use `get_feature_importance` to inspect coefficients. Positive coefficients push the model toward one class; negative coefficients push it away from that class. For multiclass models, the helper averages absolute coefficient sizes across classes.

## Strengths

- Easy to explain.
- Fast to train.
- Gives probabilities.
- Good baseline classifier.
- Coefficients can support interpretation.

## Limitations

- Assumes a mostly linear boundary between classes.
- Can underfit complex patterns.
- Needs careful interpretation when features are correlated.
- Classification threshold may need adjustment for policy decisions.

## Common Mistakes

- Using logistic regression for a continuous numeric target.
- Judging an imbalanced classifier by accuracy only.
- Treating probability as certainty.
- Forgetting that a high-risk classification target must be created carefully before modeling.

## Useful Links

- scikit-learn logistic regression guide: https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression
- scikit-learn `LogisticRegression`: https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html
- Google ML Crash Course, logistic regression: https://developers.google.com/machine-learning/crash-course/logistic-regression
- Google ML Crash Course, classification: https://developers.google.com/machine-learning/crash-course/classification

