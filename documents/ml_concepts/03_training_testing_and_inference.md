# Training, Testing, And Inference

Training and inference are two different phases of machine learning.

Training is when the model learns from data.

Inference is when the trained model is used to produce an output for data.

## Training

Training is the process of fitting a model.

In supervised learning, training data includes features and labels:

```text
features + known labels -> training algorithm -> trained model
```

Example:

```text
past intersection features + known crash counts -> train model -> crash-count prediction model
```

During training, the model changes its internal parameters so its predictions are closer to the known labels.

## Testing

Testing checks how the trained model performs on data it did not use for training.

This is important because a model can memorize training data. A memorized model may look good during training but fail on new examples.

Typical split:

```text
80 percent training data
20 percent testing data
```

The exact split depends on the dataset size and project needs.

## Validation

Validation is another evaluation step often used for choosing model settings.

Common setup:

- Training set: fit the model.
- Validation set: choose model type or hyperparameters.
- Test set: final performance check.

In smaller student projects, a simple train/test split may be enough. In larger projects, validation or cross-validation is usually better.

## Inference

Inference means using a trained model to produce an output.

Examples:

```text
trained crash model + new intersection features -> predicted crash count
```

```text
trained classifier + road segment features -> high congestion or not high congestion
```

```text
trained language model + text prompt -> generated answer
```

Inference does not usually change the model. It applies the model.

## Prediction Versus Decision

A prediction is the model output.

A decision is what a human or system does with that output.

Example:

```text
Prediction: this intersection has 0.72 probability of high crash risk.
Decision: add it to a safety review list.
```

The decision should consider more than the model:

- Budget
- Equity
- Engineering judgment
- Field review
- Public input
- Policy priorities

## Training Process Step By Step

1. Choose a clear question.
2. Collect and clean data.
3. Create features.
4. Choose the label, if supervised.
5. Split into training and testing data.
6. Fit the model on the training data.
7. Make predictions on the test data.
8. Evaluate performance.
9. Explain errors and important features.
10. Use the trained model for inference, if appropriate.

## Overfitting And Underfitting

Overfitting means the model learns the training data too closely and performs poorly on new data.

Example:

```text
A very deep tree memorizes individual road segments instead of learning general congestion patterns.
```

Underfitting means the model is too simple to capture the real pattern.

Example:

```text
A straight-line model misses important threshold effects in crash risk.
```

A good model balances both.

## Common Mistakes

- Evaluating the model only on training data.
- Using test data to choose model settings and then reporting the same test score as final.
- Confusing inference with training.
- Treating a prediction as an automatic decision.
- Forgetting that future data may differ from historical training data.

## Useful Links

- Google ML Crash Course, datasets and generalization: https://developers.google.com/machine-learning/crash-course/overfitting
- scikit-learn model selection and evaluation: https://scikit-learn.org/stable/model_selection.html
- scikit-learn train/test split: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html

