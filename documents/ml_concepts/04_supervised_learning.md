# Supervised Learning

Supervised learning is machine learning with known answers.

The model learns from examples where each row has:

- Features: the input columns.
- Label: the answer column.

The goal is to learn a pattern that can predict the label for new rows.

## Simple Definition

```text
features + known label -> train model
new features -> trained model -> predicted label
```

## Example

Suppose each row is a road segment.

Features:

- Traffic volume
- Speed limit
- Lane count
- Truck share
- Road class

Label:

- Speed ratio

The model learns from road segments where the speed ratio is already known. Then it predicts speed ratio for other road segments.

## Main Types Of Supervised Learning

Regression predicts a number.

Examples:

- Crash count
- Speed ratio
- Traffic volume
- Travel time
- Auto commute share

Classification predicts a category.

Examples:

- High crash risk or not high crash risk
- Low, medium, or high congestion
- Priority or not priority
- Road class

## Why It Is Called Supervised

It is called supervised because the known labels act like a teacher. The model makes predictions during training, compares them to the known labels, and adjusts to reduce errors.

The supervision comes from the labeled examples.

## Supervised Learning Workflow

1. Choose a target label.
2. Choose features that may help predict the label.
3. Prepare the data.
4. Split the data into training and testing sets.
5. Train the model on the training set.
6. Predict labels for the test set.
7. Compare predictions to known test labels.
8. Interpret performance and errors.

## Transportation Examples

Regression question:

```text
Can road characteristics predict average speed ratio?
```

Classification question:

```text
Can intersection characteristics predict whether an intersection is high crash risk?
```

Another classification question:

```text
Can tract characteristics predict whether a tract has low auto commute share?
```

## Common Supervised Models

Regression models:

- Linear regression
- Ridge regression
- Lasso regression
- Decision tree regression
- Random forest regression
- Gradient boosting regression

Classification models:

- Logistic regression
- Decision tree classifier
- Random forest classifier
- Gradient boosting classifier
- K-nearest neighbors
- Support vector machine

See `documents/ml_algorithms` for algorithm-specific guides.

## Strengths

- Directly predicts an outcome of interest.
- Easy to evaluate because known labels exist.
- Useful for planning and screening questions.
- Can compare several models with the same metrics.

## Limitations

- Requires labels.
- Labels may be noisy, biased, or incomplete.
- A model can learn historical bias.
- Good prediction does not automatically prove causation.
- A model may fail when future conditions differ from training data.

## Common Mistakes

- Calling a clustering task supervised when there is no label.
- Using the target label as one of the features.
- Evaluating on the same data used for training.
- Using accuracy alone for imbalanced classification.
- Treating model output as the final decision.

## Useful Links

- Google Machine Learning Crash Course: https://developers.google.com/machine-learning/crash-course/
- scikit-learn supervised learning guide: https://scikit-learn.org/stable/supervised_learning.html

