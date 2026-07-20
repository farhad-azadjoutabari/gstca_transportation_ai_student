# What Is A Model?

In machine learning, a model is a learned pattern that maps inputs to an output.

The inputs are usually called features. The output might be a prediction, a class, a cluster label, a probability, or generated content.

## Simple Definition

A model is a function learned from data.

```text
features -> model -> output
```

Example:

```text
road features -> model -> predicted speed ratio
```

Or:

```text
intersection features -> model -> high crash risk probability
```

## Model Versus Algorithm

The algorithm is the method used to learn.

The model is the result after learning.

Example:

```text
Algorithm: random forest
Training data: past road segment records
Trained model: a fitted random forest that predicts congestion
```

A helpful analogy:

- Recipe: algorithm
- Ingredients: data
- Finished dish: trained model

## Parameters Versus Hyperparameters

Parameters are learned by the model during training.

Examples:

- Linear regression coefficients
- Decision tree split rules
- Neural network weights

Hyperparameters are settings chosen before or during training by the analyst.

Examples:

- Number of trees in a random forest
- Maximum tree depth
- K in K-Means
- Learning rate in gradient boosting

The model learns parameters. The analyst chooses or tunes hyperparameters.

## Model Inputs And Outputs

Regression model:

```text
Inputs: traffic volume, speed limit, lane count
Output: predicted crash count
```

Classification model:

```text
Inputs: traffic volume, speed limit, lane count
Output: high crash risk or not high crash risk
```

Clustering model:

```text
Inputs: density, income, transit access, land use
Output: cluster label
```

Generative model:

```text
Input: a prompt asking for a summary
Output: generated text
```

## A Model Is Not The Same As The Real World

A model is a simplified representation. It can be useful without being perfect.

For example, a crash prediction model might identify high-risk patterns, but crashes are affected by many factors that may not be in the dataset:

- Driver behavior
- Weather
- Temporary construction
- Signal timing changes
- Reporting practices
- Random variation

This is why model results should be interpreted carefully.

## What Makes A Model Useful?

A useful model should:

- Address a clear question.
- Be trained on relevant data.
- Perform better than a simple baseline.
- Be evaluated on data it did not train on.
- Use features that make sense for the problem.
- Be understandable enough for the decision context.
- Have limitations clearly explained.

## Model As Equation, Tree, Distance Rule, Or Neural Network

Different algorithms produce different kinds of models.

Linear regression creates an equation.

Decision trees create a sequence of split rules.

KNN stores examples and compares distances.

K-Means stores cluster centers.

Neural networks learn many connected weights.

Large language models learn patterns in tokens and generate likely next tokens based on context.

## Common Mistakes

- Saying "the algorithm predicted" when the trained model made the prediction.
- Treating a model as objective truth.
- Judging a model only by how complex it sounds.
- Ignoring the difference between learned parameters and chosen hyperparameters.
- Forgetting that a model can work on past data and still fail on future data if conditions change.

## Useful Links

- Google Machine Learning Crash Course: https://developers.google.com/machine-learning/crash-course/
- scikit-learn choosing the right estimator: https://scikit-learn.org/stable/machine_learning_map.html

