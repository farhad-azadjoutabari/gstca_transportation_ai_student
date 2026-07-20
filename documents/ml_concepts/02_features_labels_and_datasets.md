# Features, Labels, And Datasets

Machine learning starts with data. In most beginner ML projects, the data is organized as a table.

Each row is one example.

Each column describes something about the example.

## Examples, Features, And Labels

An example is one row in the dataset.

For transportation projects, one example might be:

- One Census tract
- One road segment
- One intersection
- One crash record
- One trip
- One employer location

A feature is an input column the model can use.

Examples:

- Population density
- Traffic volume
- Speed limit
- Number of lanes
- Bus stop count
- Median income
- Road class

A label is the answer column the model is trying to predict in supervised learning.

Examples:

- `crash_count`
- `speed_ratio`
- `high_crash_risk`
- `congestion_class`
- `auto_commute_share`

## X And y

Many ML tools use these names:

- `X`: the feature table.
- `y`: the label or target column.

Example:

```text
X = population, bus stop count, income, employment density
y = auto commute share
```

If there is no `y`, the task may be unsupervised learning.

## Label Types

The label type helps decide the ML task.

Numeric label:

```text
crash_count = 0, 1, 2, 3, ...
speed_ratio = 0.45, 0.81, 0.96, ...
```

This usually means regression.

Categorical label:

```text
high_crash_risk = yes or no
congestion_class = low, medium, high
```

This usually means classification.

No label:

```text
Only features are available.
```

This may mean clustering, PCA, anomaly detection, or another unsupervised task.

## Feature Types

Numeric features are numbers.

Examples:

- `population`
- `aadt`
- `speed_limit`
- `lane_count`

Categorical features are groups or names.

Examples:

- `road_class`
- `signal_type`
- `land_use_category`

Boolean features are true/false or 0/1.

Examples:

- `has_signal`
- `has_crosswalk`
- `is_high_crash`

Text features are longer written values.

Examples:

- Crash narrative
- Public comment
- Project description

Geographic features are spatial information.

Examples:

- Geometry column
- Latitude and longitude
- Distance to rail station
- Count of bus stops within half a mile

Most basic ML helpers use tabular numeric and categorical features. Geometry is usually used first to create meaningful features, not included directly as a model input.

## What Makes A Good Feature?

A good feature should:

- Be available at prediction time.
- Be related to the question.
- Be measured consistently.
- Not leak the answer.
- Be understandable enough to explain.

Example of a useful feature:

```text
traffic_volume
```

Example of leakage:

```text
crash_rate_category created from crash_count, then used to predict crash_count
```

The model would be given the answer indirectly.

## Training Data And New Data

Training data is used to fit the model.

New data is used after training for inference.

The new data must have the same kinds of features as the training data.

Example:

If a crash-risk model was trained using:

- `aadt`
- `speed_limit`
- `lane_count`
- `signal_type`

Then new intersections also need those columns before the model can predict risk.

## Common Mistakes

- Including ID columns as features.
- Including geometry directly when the model expects numeric/categorical columns.
- Including the label inside the features.
- Using future information to predict the past.
- Treating categorical labels as numeric ranks when they are only names.
- Forgetting that missing values must be handled before modeling.

## Useful Links

- Google ML Crash Course, numerical data: https://developers.google.com/machine-learning/crash-course/numerical-data
- Google ML Crash Course, categorical data: https://developers.google.com/machine-learning/crash-course/categorical-data

