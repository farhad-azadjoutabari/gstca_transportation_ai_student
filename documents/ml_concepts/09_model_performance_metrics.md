# Model Performance Metrics

Model performance metrics measure how well a model works.

Different tasks need different metrics. Regression, classification, and clustering are evaluated in different ways.

## Why Metrics Matter

A model can sound impressive but perform poorly. Metrics help answer:

- How close are numeric predictions?
- How often are class predictions correct?
- Which classes are missed?
- Does the model beat a simple baseline?
- Are clusters separated and interpretable?

Metrics should be calculated on data the model did not train on whenever possible.

## Regression Metrics

Regression predicts numbers.

Common regression metrics:

- MAE
- MSE
- RMSE
- R2

### MAE

MAE means mean absolute error.

It is the average absolute difference between predicted and actual values.

Example:

```text
Actual crash count: 5
Predicted crash count: 3
Absolute error: 2
```

Lower MAE is better.

### MSE

MSE means mean squared error.

It squares each error before averaging. Large errors get extra penalty.

Lower MSE is better.

### RMSE

RMSE means root mean squared error.

It is the square root of MSE. It is in the same unit as the target.

Example:

```text
RMSE = 2.4 crashes
```

This is easier to interpret than MSE because it is in crash-count units.

Lower RMSE is better.

### R2

R2 measures how much variation in the target is explained by the model.

R2 can be:

- Close to 1: strong explanatory/predictive fit.
- Around 0: about as useful as predicting the mean.
- Negative: worse than predicting the mean.

Higher R2 is better, but R2 should not be the only metric.

## Classification Metrics

Classification predicts categories.

Common classification metrics:

- Accuracy
- Precision
- Recall
- F1
- ROC-AUC
- Confusion matrix

### Accuracy

Accuracy is the share of predictions that are correct.

```text
correct predictions / all predictions
```

Accuracy is easy to understand, but it can be misleading when classes are imbalanced.

Example:

If only 5 percent of intersections are high risk, a model that always predicts "not high risk" can be 95 percent accurate but useless for finding high-risk intersections.

### Precision

Precision answers:

```text
When the model predicts this class, how often is it correct?
```

High precision means fewer false alarms.

### Recall

Recall answers:

```text
Out of all true cases of this class, how many did the model find?
```

High recall means fewer missed cases.

For safety screening, recall may be especially important because missing high-risk locations can be costly.

### F1

F1 combines precision and recall into one score.

It is useful when you need balance between false alarms and missed cases.

### ROC-AUC

ROC-AUC measures how well predicted probabilities rank positive cases above negative cases.

It is often used for binary classification.

Higher ROC-AUC is better.

### Confusion Matrix

A confusion matrix shows actual classes versus predicted classes.

For binary classification:

```text
                 Predicted no   Predicted yes
Actual no        true negative  false positive
Actual yes       false negative true positive
```

This table helps show which mistakes the model makes.

## Clustering Metrics

Clustering does not have known labels, so evaluation is harder.

Common clustering checks:

- Cluster counts
- Silhouette score
- Calinski-Harabasz score
- Davies-Bouldin score
- Cluster summaries

Silhouette score measures how close rows are to their own cluster compared with other clusters. Higher is usually better.

But a good score does not guarantee the clusters make planning sense.

## Metric Choice Depends On The Goal

If exact numeric error matters, use MAE or RMSE.

If finding rare high-risk cases matters, use recall and F1.

If false alarms are expensive, check precision.

If the goal is exploration, use clustering summaries and domain judgment.

## Common Mistakes

- Using training metrics as final performance.
- Reporting only one metric.
- Using accuracy for imbalanced classification without precision, recall, or F1.
- Comparing regression and classification metrics directly.
- Choosing a model with the best score but no practical improvement over baseline.
- Reporting metrics without explaining what they mean in the project context.

## Useful Links

- scikit-learn model evaluation guide: https://scikit-learn.org/stable/modules/model_evaluation.html
- scikit-learn metrics API: https://scikit-learn.org/stable/api/sklearn.metrics.html
- Google ML Crash Course, classification: https://developers.google.com/machine-learning/crash-course/classification

