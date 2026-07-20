# ML Workflow and Data Preparation

Machine learning works best when the input table is organized clearly. In this project, that usually means one row per thing you want to study: one Census tract, road segment, intersection, employer, crash location, or corridor.

Each row should have:

- An optional ID column, such as `GEOID`, `road_id`, or `intersection_id`.
- Feature columns, which are the inputs the model is allowed to use.
- An optional target column, which is the outcome you want to predict.

For example, if each row is an intersection, feature columns might include nearby traffic volume, speed limit, number of approaches, signal type, and crosswalk count. The target column might be `crash_count` for regression or `high_crash_risk` for classification.

## What Data Preparation Means

Most ML models cannot directly use messy real-world tables. The helper function `prepare_ml_data` handles the common steps:

- Selects only the feature columns you want.
- Drops rows with missing target values, if a target is provided.
- Fills missing numeric feature values with the median.
- Fills missing categorical feature values with the most common category.
- Scales numeric features by default so columns are comparable.
- Converts text, category, and boolean columns into numeric dummy variables using one-hot encoding.
- Returns a clean numeric feature table called `X`.
- Returns the target column as `y` when a target is provided.

This matters because many ML algorithms expect numbers. A model cannot understand a raw value like `"Signalized"` unless it has been converted into numeric columns.

## Helper Function

Use:

```python
from helper.ml import prepare_ml_data
```

Implementation file:

```text
helper/ml/prepare_ml_data.py
```

The helper uses these scikit-learn tools internally:

- `ColumnTransformer` to apply different preparation steps to numeric and categorical columns.
- `SimpleImputer` to fill missing values.
- `StandardScaler` to scale numeric columns.
- `OneHotEncoder` to convert categorical columns into dummy variables.

## Basic Example

```python
from helper.ml import prepare_ml_data

features = [
    "population",
    "bus_stop_count",
    "total_employees",
    "park_acres",
    "road_class",
]

ml_data = prepare_ml_data(
    tracts,
    feature_columns=features,
    target_column="crash_count",
)

X = ml_data["X"]
y = ml_data["y"]
```

After this, `X` is a clean numeric table that can be used by regression, classification, clustering, or PCA helpers.

## What The Output Contains

`prepare_ml_data` returns a dictionary:

- `X`: prepared numeric feature table.
- `y`: target values, if `target_column` was provided.
- `raw_X`: original unprocessed feature columns.
- `data`: original rows used for modeling, after dropping missing target rows if needed.
- `preprocessor`: the fitted scikit-learn preprocessing object.
- `feature_columns`: the original feature column names.
- `target_column`: the target column name, if any.
- `numeric_columns`: columns treated as numeric.
- `categorical_columns`: columns treated as categorical.

## Regression, Classification, Clustering, And PCA

For regression or classification, include `target_column`:

```python
ml_data = prepare_ml_data(
    analysis_df,
    feature_columns=features,
    target_column="speed_ratio",
)
```

For clustering or PCA, leave `target_column=None`:

```python
cluster_data = prepare_ml_data(
    analysis_df,
    feature_columns=features,
)
```

## Numeric And Categorical Columns

Usually, the helper detects them automatically. Numeric columns stay numeric. Text, category, and boolean columns are treated as categorical.

If the automatic choice is not right, you can be explicit:

```python
ml_data = prepare_ml_data(
    roads,
    feature_columns=["aadt", "speed_limit", "road_class"],
    target_column="speed_ratio",
    numeric_columns=["aadt", "speed_limit"],
    categorical_columns=["road_class"],
)
```

## Why Scaling Matters

Scaling changes numeric columns so they are measured on a comparable scale. This is very important for algorithms that use distances, such as K-Means, DBSCAN, KNN, SVM, and PCA.

Without scaling, a large-number column like population could dominate a small-number column like park acres, even if both are important.

The helper uses `scale_numeric=True` by default. You can turn it off:

```python
ml_data = prepare_ml_data(
    tracts,
    feature_columns=features,
    target_column="crash_count",
    scale_numeric=False,
)
```

For most student projects, keep scaling on.

## Common Mistakes

- Do not include geometry columns in `feature_columns`.
- Do not include ID columns as model features unless the ID has real meaning. IDs often teach the model row labels instead of relationships.
- Do not include the target column inside `feature_columns`.
- Avoid features that leak the answer. For example, do not predict `crash_count` using a column that was calculated directly from `crash_count`.
- Make sure the target matches the task. Use a number for regression and a category or flag for classification.

## Useful Links

- scikit-learn preprocessing guide: https://scikit-learn.org/stable/modules/preprocessing.html
- scikit-learn imputation guide: https://scikit-learn.org/stable/modules/impute.html
- Google ML Crash Course, working with numerical data: https://developers.google.com/machine-learning/crash-course/numerical-data
- Google ML Crash Course, working with categorical data: https://developers.google.com/machine-learning/crash-course/categorical-data

