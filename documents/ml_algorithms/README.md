# Machine Learning Algorithm Guides

This folder explains the machine learning models and algorithms available through the repository's `helper.ml` functions. The goal is to make the ideas understandable for students who are new to machine learning, while also showing exactly how to run each method with the helper code.

Start with these workflow guides:

- [ML Workflow and Data Preparation](00_ml_workflow_and_data_preparation.md)
- [Train/Test Split and Evaluation](01_train_test_split_and_evaluation.md)
- [Baseline Models](02_baseline_models.md)
- [Model Comparison Helpers](20_model_comparison_helpers.md)
- [Feature Importance and Model Explanation](19_feature_importance_and_model_explanation.md)

Supervised learning guides:

- [Linear Regression](03_linear_regression.md)
- [Ridge Regression](04_ridge_regression.md)
- [Lasso Regression and Feature Selection](05_lasso_regression_and_feature_selection.md)
- [Logistic Regression](06_logistic_regression.md)
- [Decision Trees](07_decision_trees.md)
- [Random Forest](08_random_forest.md)
- [Extra Trees](09_extra_trees.md)
- [Gradient Boosting](10_gradient_boosting.md)
- [Histogram Gradient Boosting](11_hist_gradient_boosting.md)
- [K-Nearest Neighbors](12_k_nearest_neighbors.md)
- [Support Vector Machines](13_support_vector_machines.md)

Unsupervised learning and dimensionality reduction guides:

- [K-Means Clustering](14_kmeans_clustering.md)
- [DBSCAN Clustering](15_dbscan_clustering.md)
- [Hierarchical Clustering](16_hierarchical_clustering.md)
- [Gaussian Mixture Models](17_gaussian_mixture_models.md)
- [Principal Component Analysis](18_principal_component_analysis.md)

## How These Guides Match The Helper Code

The helper functions live in `helper/ml`. The most important student-facing functions are:

- `prepare_ml_data`: prepares features for any ML task.
- `split_train_test`: creates training and testing datasets for supervised learning.
- `run_regression_model`: trains one regression model.
- `run_classification_model`: trains one classification model.
- `compare_regression_models`, `compare_classification_models`, and `compare_models`: compare several models.
- `run_kmeans_clustering`, `run_dbscan_clustering`, `run_hierarchical_clustering`, and `run_gaussian_mixture_clustering`: run clustering.
- `find_best_k_for_kmeans`, `evaluate_clustering`, and `summarize_clusters`: choose and explain clusters.
- `run_pca`: reduce many columns into a smaller number of components.
- `evaluate_regression`, `evaluate_classification`, `get_feature_importance`, `explain_model_results`, and `predict_with_model`: evaluate, explain, and apply fitted models.

The guides focus on algorithms exposed by `helper.ml`. If a notebook uses an algorithm directly from scikit-learn that is not wrapped in `helper.ml`, the workflow still applies, but the exact helper call may differ.

## Quick Decision Guide

Use regression when the target is a number, such as crash count, speed ratio, traffic volume, travel time, or mode share.

Use classification when the target is a category, such as high crash risk, low/medium/high congestion, priority or not priority, or transit access class.

Use clustering when there is no target column and the goal is to find groups of similar records, such as similar tracts, roads, intersections, employers, or crash locations.

Use PCA when there are many related numeric features and you want to simplify them for visualization, clustering, or interpretation.

Use feature importance after a model is trained, when you want to explain which variables influenced the model most.

## Useful General Links

- scikit-learn User Guide: https://scikit-learn.org/stable/user_guide.html
- scikit-learn algorithm cheat sheet: https://scikit-learn.org/stable/machine_learning_map.html
- scikit-learn model evaluation guide: https://scikit-learn.org/stable/modules/model_evaluation.html
- Google Machine Learning Crash Course: https://developers.google.com/machine-learning/crash-course/
- scikit-learn external resources, videos, and MOOC: https://scikit-learn.org/stable/presentations.html

