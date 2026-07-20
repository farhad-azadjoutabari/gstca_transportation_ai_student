# Machine Learning Big Picture

Machine learning, often shortened to ML, is a way for computers to learn patterns from data instead of being given every rule by hand.

Traditional programming often looks like this:

```text
human writes rules + data -> computer gives answer
```

Machine learning often looks like this:

```text
data + known answers -> computer learns a model
model + new data -> computer gives prediction
```

## A Simple Example

Suppose you want to identify intersections that may have high crash risk.

You could write manual rules:

```text
If traffic volume is high and speed limit is high, mark high risk.
```

That can be useful, but real patterns are usually more complicated. A machine learning model can learn from many past intersections:

- Traffic volume
- Speed limit
- Number of lanes
- Signal type
- Crosswalk count
- Nearby transit stops
- Past crash count or high-risk label

The model looks for patterns that connect the inputs to the outcome.

## Machine Learning Is Not Magic

ML does not "understand" a city the way a planner or engineer does. It finds statistical patterns in examples. If the examples are incomplete, biased, noisy, or poorly prepared, the model can learn weak or misleading patterns.

Good ML work still needs:

- A clear question
- Good data
- Thoughtful feature selection
- Evaluation on data the model did not train on
- Human interpretation
- Domain knowledge

## The Main Types Of ML

There are several major learning types:

- Supervised learning: the model learns from examples with known answers.
- Unsupervised learning: the model looks for patterns without known answers.
- Semi-supervised learning: the model uses a small labeled dataset and a larger unlabeled dataset.
- Reinforcement learning: an agent learns by taking actions and receiving rewards or penalties.
- Generative AI: models create new content, such as text, images, audio, code, or synthetic data.

These types can overlap. For example, generative AI models are often trained with self-supervised learning and may be improved with reinforcement learning from feedback.

## Prediction Versus Explanation

A model can be good at prediction without giving a simple explanation.

Example:

```text
The model predicts high crash risk accurately, but it is hard to explain exactly why for each intersection.
```

Another model may be easier to explain but less accurate:

```text
Logistic regression is easier to interpret, but it may miss nonlinear patterns.
```

In student projects, it is important to discuss both:

- How well the model performs.
- Whether the model behavior makes sense.

## Common ML Workflow

Most ML projects follow this pattern:

1. Define the question.
2. Create an analysis table.
3. Choose features and, if supervised, a label.
4. Prepare the data.
5. Split into training and testing data.
6. Train one or more models.
7. Evaluate model performance.
8. Explain the model results.
9. Use the model for inference, if appropriate.
10. Communicate limitations.

## Transportation Examples

Regression:

```text
Predict the number of crashes at each intersection.
```

Classification:

```text
Predict whether each road segment is high congestion or not high congestion.
```

Clustering:

```text
Group Census tracts into similar neighborhood types based on density, income, land use, and transit access.
```

PCA:

```text
Reduce many related demographic variables into a smaller number of summary components.
```

Generative AI:

```text
Draft a plain-language summary of model findings, generate synthetic example scenarios, or answer questions about a project report.
```

## What ML Can And Cannot Do

ML can:

- Find patterns in large tables.
- Predict numeric outcomes or categories.
- Group similar records.
- Help identify unusual records.
- Support decision-making.
- Generate text, images, code, and other content.

ML cannot automatically:

- Prove causation.
- Fix poor data quality.
- Replace domain expertise.
- Decide what is fair or ethical.
- Guarantee accurate predictions for future conditions unlike the training data.

## Useful Links

- Google Machine Learning Crash Course: https://developers.google.com/machine-learning/crash-course/
- scikit-learn User Guide: https://scikit-learn.org/stable/user_guide.html
- Google clustering course: https://developers.google.com/machine-learning/clustering

