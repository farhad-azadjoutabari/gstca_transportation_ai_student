# Common ML Terms

This page explains common machine learning terms in short, plain language.

## Accuracy

Accuracy is the share of classification predictions that are correct.

It can be misleading when one class is much more common than another.

## Algorithm

An algorithm is the method used to learn a model.

Example:

```text
Random forest is an algorithm.
The fitted random forest is the trained model.
```

## Baseline

A baseline is a simple reference model.

Example:

```text
A regression baseline might always predict the average crash count.
```

A useful model should usually beat the baseline.

## Bias

Bias can mean different things.

In model evaluation, high bias often means the model is too simple and underfits.

In social or ethical analysis, bias can mean unfair or systematic differences in data, model behavior, or outcomes.

Always clarify which meaning is being used.

## Classification

Classification predicts a category.

Example:

```text
high crash risk / not high crash risk
```

## Clustering

Clustering groups similar rows without using a known label.

Example:

```text
Group similar tracts into neighborhood types.
```

## Cross-Validation

Cross-validation evaluates a model by training and testing it on several different splits of the data.

It gives a more stable performance estimate than one train/test split, especially for smaller datasets.

## Embedding

An embedding is a numeric vector that represents meaning or similarity.

Example:

```text
Two public comments with similar meanings should have similar embeddings.
```

## Epoch

An epoch is one full pass through the training data during neural network training.

## Feature

A feature is an input column used by the model.

Example:

```text
speed_limit
aadt
bus_stop_count
```

## Fine-Tuning

Fine-tuning adapts an already trained model to a more specific task or style using additional examples.

## Generative AI

Generative AI creates new content, such as text, images, code, audio, video, or synthetic data.

## Ground Truth

Ground truth means the best available known answer.

Example:

```text
Observed crash count is the ground truth for a crash-count prediction task.
```

Ground truth can still be noisy if the source data has errors.

## Hallucination

A hallucination is generated content that sounds plausible but is false, unsupported, or invented.

This term is usually used with generative AI.

## Hyperparameter

A hyperparameter is a model setting chosen before or during training.

Examples:

- Number of trees
- Maximum tree depth
- Learning rate
- Number of clusters

## Inference

Inference means using a trained model to produce output.

Examples:

```text
Use a fitted random forest to predict crash count.
Use a language model to answer a prompt.
```

Inference is application, not full retraining.

## Label

A label is the answer column in supervised learning.

Example:

```text
crash_count
high_crash_risk
speed_ratio
```

## Leakage

Leakage happens when information from the answer sneaks into the features.

Example:

```text
Using crash_rate_category to predict crash_count.
```

Leakage can make model performance look much better than it really is.

## Loss

Loss measures how wrong the model is during training.

The training process tries to reduce loss.

## Model

A model is the learned pattern used to make predictions, assign clusters, or generate outputs.

## Overfitting

Overfitting means the model memorizes training data too closely and performs poorly on new data.

## Parameter

A parameter is a value the model learns during training.

Examples:

- Linear regression coefficient
- Neural network weight
- Tree split rule

## Precision

Precision answers:

```text
When the model predicts a class, how often is it right?
```

High precision means fewer false positives.

## Prompt

A prompt is the input instruction or question given to a generative AI model.

## Recall

Recall answers:

```text
Out of all true cases, how many did the model find?
```

High recall means fewer false negatives.

## Regression

Regression predicts a number.

Example:

```text
predicted crash count = 2.6
```

## RAG

RAG means Retrieval-Augmented Generation.

It combines search over trusted documents with generative AI.

## Target

Target is another word for label.

## Test Set

The test set is held-out data used to evaluate a trained model.

## Token

A token is a small unit of text used by a language model. A token can be a word, part of a word, punctuation, or another text unit depending on the tokenizer.

## Training

Training is the process of fitting a model to data.

## Training Set

The training set is the data used to fit the model.

## Underfitting

Underfitting means the model is too simple to capture the pattern.

## Validation Set

A validation set is data used to choose model settings before final testing.

## Variance

In model evaluation, high variance means the model is too sensitive to the particular training data and may overfit.

## Useful Links

- Google Machine Learning Crash Course: https://developers.google.com/machine-learning/crash-course/
- scikit-learn User Guide: https://scikit-learn.org/stable/user_guide.html
- scikit-learn model evaluation guide: https://scikit-learn.org/stable/modules/model_evaluation.html

