# Regression Versus Classification

Regression and classification are both supervised learning tasks. The difference is the label type.

Regression predicts a numeric label.

Classification predicts a categorical label.

## The Key Difference

```text
Regression label = number
Classification label = category
```

This is the most important distinction.

## Regression

Regression is used when the answer is a number.

Examples:

- `crash_count = 3`
- `speed_ratio = 0.74`
- `traffic_volume = 28500`
- `auto_commute_share = 61.2`
- `travel_time_minutes = 28`

Regression output can usually move along a continuous scale or count scale.

Example question:

```text
How many crashes are expected at this intersection?
```

Possible output:

```text
2.6 predicted crashes
```

Even if actual crash counts are whole numbers, a regression model may predict decimals because it is estimating an expected value.

## Classification

Classification is used when the answer is a category.

Examples:

- `high_crash_risk = yes` or `no`
- `congestion_class = low`, `medium`, or `high`
- `priority_status = priority` or `not priority`
- `road_type = motorway`, `primary`, `secondary`, or `tertiary`

Example question:

```text
Is this intersection high crash risk?
```

Possible output:

```text
high_crash_risk
```

Many classifiers can also output probabilities:

```text
0.78 probability of high crash risk
```

## Binary, Multiclass, And Multilabel Classification

Binary classification has two classes.

Example:

```text
high crash risk / not high crash risk
```

Multiclass classification has more than two possible classes, but each row has one class.

Example:

```text
low / medium / high congestion
```

Multilabel classification allows more than one label per row.

Example:

```text
one project can be tagged as safety, transit, and freight
```

Most beginner transportation examples use binary or multiclass classification.

## Same Data, Different Framing

The same real-world question can sometimes be framed as regression or classification.

Crash example:

Regression:

```text
Predict crash_count.
```

Classification:

```text
Predict whether crash_count is in the top 25 percent.
```

Congestion example:

Regression:

```text
Predict speed_ratio.
```

Classification:

```text
Predict low, medium, or high congestion.
```

The best framing depends on the decision you want to support.

## Metrics Are Different

Regression metrics measure numeric error:

- MAE
- MSE
- RMSE
- R2

Classification metrics measure category correctness:

- Accuracy
- Precision
- Recall
- F1
- ROC-AUC
- Confusion matrix

Do not compare regression RMSE to classification accuracy. They answer different questions.

## Choosing Between Regression And Classification

Choose regression when:

- The exact numeric value matters.
- You care about size or amount.
- The label is naturally numeric.

Choose classification when:

- The decision is category-based.
- You need a yes/no or low/medium/high result.
- You want to screen or prioritize records.
- The numeric outcome is too noisy but broad categories are useful.

## Common Mistakes

- Using classification for a numeric target without creating categories first.
- Treating category numbers as numeric values. For example, road class codes may be names, not quantities.
- Using regression metrics for classification.
- Using classification accuracy for imbalanced risk screening without checking recall and F1.
- Forgetting that turning a number into categories loses information.

## Useful Links

- Google ML Crash Course, linear regression: https://developers.google.com/machine-learning/crash-course/linear-regression
- Google ML Crash Course, classification: https://developers.google.com/machine-learning/crash-course/classification
- scikit-learn model evaluation guide: https://scikit-learn.org/stable/modules/model_evaluation.html

