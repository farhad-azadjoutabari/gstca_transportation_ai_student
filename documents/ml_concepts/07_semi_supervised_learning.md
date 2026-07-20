# Semi-Supervised Learning

Semi-supervised learning uses both labeled and unlabeled data.

It is useful when labels are expensive or slow to create, but unlabeled data is easy to collect.

## Simple Definition

```text
small labeled dataset + large unlabeled dataset -> model learns better patterns
```

## Why It Exists

Supervised learning needs labels. But labeling data can be difficult.

Example:

You may have thousands of road segments with features, but only a few have been manually reviewed and labeled as high safety concern or not high safety concern.

Semi-supervised learning tries to use both:

- The small set with labels.
- The large set without labels.

## Example

Suppose you have:

- 500 intersections manually labeled as high risk or not high risk.
- 20,000 intersections with features but no risk label.

A semi-supervised method can learn from the labeled examples while also using the structure of the unlabeled examples.

## Common Approaches

Self-training:

1. Train a model on labeled data.
2. Use it to predict labels for unlabeled data.
3. Add the most confident predictions as pseudo-labels.
4. Retrain the model with the expanded dataset.

Label propagation:

```text
Similar records are encouraged to share similar labels.
```

Consistency training:

```text
The model should make similar predictions even when an input is slightly changed.
```

## Pseudo-Labels

A pseudo-label is a label predicted by a model, not confirmed by a human.

Example:

```text
The model predicts that an unlabeled intersection has 0.96 probability of high crash risk.
The analyst may use "high crash risk" as a pseudo-label during training.
```

Pseudo-labels can help, but they can also spread model mistakes.

## When To Use It

Use semi-supervised learning when:

- Labels are limited.
- Unlabeled examples are plentiful.
- Similar records likely have similar labels.
- You can tolerate careful experimentation and validation.

## Strengths

- Can use more data than supervised learning alone.
- Helpful when labeling is expensive.
- Can improve performance when unlabeled data has useful structure.

## Limitations

- More complex than ordinary supervised learning.
- Bad pseudo-labels can reinforce errors.
- Evaluation still needs trustworthy labeled test data.
- Results depend on assumptions about similarity and data structure.

## Transportation Examples

Possible uses:

- Label a small set of public comments by topic, then use many unlabeled comments to improve classification.
- Label some crash narratives by contributing factor, then learn from many unlabeled narratives.
- Label a subset of locations as priority candidates, then use unlabeled locations to improve screening.

For tabular challenge notebooks in this repository, students will usually use supervised or unsupervised learning instead. Semi-supervised learning is useful to know conceptually, but it is less common in the helper functions.

## Common Mistakes

- Treating pseudo-labels as ground truth.
- Evaluating on pseudo-labeled data instead of human-labeled test data.
- Assuming more unlabeled data always helps.
- Using semi-supervised learning when labels are already plentiful.

## Useful Links

- scikit-learn semi-supervised learning guide: https://scikit-learn.org/stable/modules/semi_supervised.html
- Google Machine Learning Crash Course: https://developers.google.com/machine-learning/crash-course/

