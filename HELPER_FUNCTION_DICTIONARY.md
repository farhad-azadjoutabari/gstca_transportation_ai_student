# Helper Function Dictionary

This file explains the helper functions available in the `helper` folder. The
helpers are organized by subfolder, matching how students import them in
notebooks.

Most students will use these imports:

```python
from helper.data_read import read_csv_file, read_shp_file, read_geojson_file, read_gpkg_file, read_large_csv_in_chunks
from helper.spatial import summarize_gdf, spatial_join, summarize_points_by_polygon, calculate_facility_coverage, prepare_spatial_data
from helper.visualization import plot_choropleth, plot_layers, plot_points
from helper.ml import prepare_ml_data, run_kmeans_clustering, compare_models, explain_model_results
from helper.eda import summarize_columns, correlation_table, compare_groups
from helper.features import create_rate, create_binary_flag, calculate_land_use_mix
from helper.similarity import compare_similar_records, rank_unexpected_outcomes
from helper.transportation import calculate_mode_share, calculate_speed_ratio, aggregate_od_flows
from helper.safety import read_txdot_crashes, summarize_crashes_by_area, summarize_crashes_by_intersection
```

## `helper/data_read`

Use these functions when loading files from the `data` folder into Python.
They add simple file checks before calling Pandas or GeoPandas.

| Function | What it does | When students should use it |
| --- | --- | --- |
| `read_csv_file(file_path, **kwargs)` | Reads a `.csv` file into a Pandas DataFrame. | Use for tabular datasets such as Census tables, OD matrices, land-use CSV exports, spending tables, crash tables, and weather tables. Students can pass normal `pandas.read_csv` options such as `skiprows=1` or `usecols=[...]`. |
| `read_large_csv_in_chunks(file_path, chunk_size=100000, groupby_columns=None, sum_columns=None, mean_columns=None, count_column=None, ...)` | Reads a large CSV in chunks and can return a grouped summary without loading the full file into memory. | Use for large OD, traffic count, TMC, or turning-movement files. If no aggregation is requested, it returns a pandas chunk iterator. |
| `read_shp_file(file_path, **kwargs)` | Reads a `.shp` shapefile into a GeoPandas GeoDataFrame. | Use for spatial layers stored as shapefiles, such as bus stops, speed limits, school zones, traffic signs, congestion polygons, or other GIS layers. |
| `read_geojson_file(file_path, **kwargs)` | Reads a `.geojson` or `.json` spatial file into a GeoPandas GeoDataFrame. | Use for spatial layers stored as GeoJSON, such as bikeways or trails. |
| `read_gpkg_file(file_path, layer=None, **kwargs)` | Reads a `.gpkg` GeoPackage into a GeoPandas GeoDataFrame. | Use for GeoPackage datasets such as employers, development, parks, rail stations, EV stations, or roadway GeoPackages. If the file has multiple layers, pass `layer="layer_name"`. |

Example:

```python
from helper.data_read import read_csv_file, read_shp_file

income = read_csv_file("data/census_demographic_2024/census_tract_income_in_past_12_months_2024/ACSST5Y2024.S1901-Data.csv")
bus_stops = read_shp_file("data/dallas_dart_bus/Dallas-DART-Stops/Bus_Stops.shp")
origin_summary = read_large_csv_in_chunks(
    "data/large_od_file.csv",
    groupby_columns="origin_trct_2020",
    count_column="sample_records",
)
```

## `helper/spatial`

Use these functions with GeoPandas GeoDataFrames. They help students inspect,
clean, measure, join, summarize, map, and save spatial datasets.

### Inspecting and Cleaning Spatial Data

| Function | What it does | When students should use it |
| --- | --- | --- |
| `summarize_gdf(gdf)` | Returns a dictionary with row count, column names, CRS, geometry types, missing values, empty geometry count, and map bounds. | Use right after reading any spatial file to understand what is in the dataset before analysis. |
| `check_crs(gdf)` | Returns CRS details, including EPSG code, whether the CRS is geographic or projected, and the coordinate unit. | Use before measuring area, measuring length, buffering, or joining two spatial datasets. |
| `drop_empty_geometries(gdf, reset_index=True)` | Removes rows where geometry is missing or empty. | Use when a dataset causes errors in mapping, clipping, spatial joins, buffers, or distance calculations. |
| `prepare_spatial_data(gdf, input_crs=None, projected_epsg=None, ...)` | Assigns a missing CRS, sets the active geometry, drops empty geometries, optionally repairs invalid geometries, and projects to a local CRS. | Use as a first cleanup step before buffers, nearest-distance joins, length, area, or overlap calculations. |

Example:

```python
from helper.data_read import read_shp_file
from helper.spatial import summarize_gdf, check_crs, drop_empty_geometries
from helper.spatial import prepare_spatial_data

roads = read_shp_file("data/speed_limits_city_of_dallas/Speed_Limits.shp")
summary = summarize_gdf(roads)
crs_info = check_crs(roads)
roads = prepare_spatial_data(roads, projected_epsg=2276)
```

### Coordinate Systems, Measurement, and Buffers

| Function | What it does | When students should use it |
| --- | --- | --- |
| `reproject_gdf(gdf, epsg)` | Reprojects a GeoDataFrame to another EPSG code. | Use when two spatial datasets have different CRS values or when data must be projected before measuring distance or area. |
| `calculate_area(gdf, column_name="area", unit="square_meters", projected_epsg=None)` | Adds an area column to polygon data. | Use for polygons such as parks, tracts, parcels, zones, airports, land-use areas, or congestion polygons. Pass a local projected EPSG code when data is in longitude/latitude. |
| `calculate_length(gdf, column_name="length", unit="meters", projected_epsg=None)` | Adds a length column to line data. | Use for lines such as roads, trails, bikeways, bus routes, truck restrictions, or network links. Pass a local projected EPSG code when data is in longitude/latitude. |
| `buffer_features(gdf, distance, projected_epsg=None)` | Creates buffer polygons around each feature. | Use to create areas within a distance of features, such as a half-mile buffer around rail stations or a 500-foot buffer around roads. |

Example:

```python
from helper.spatial import calculate_area, calculate_length, buffer_features

parks = calculate_area(parks, column_name="park_acres", unit="acres", projected_epsg=2276)
trails = calculate_length(trails, column_name="trail_miles", unit="miles", projected_epsg=2276)
station_buffers = buffer_features(stations, distance=2640, projected_epsg=2276)
```

### Basic Spatial Joins and Nearest Features

| Function | What it does | When students should use it |
| --- | --- | --- |
| `spatial_join(left_gdf, right_gdf, predicate="intersects", how="left")` | Attaches columns from one spatial dataset to another based on a spatial relationship. | Use for simple joins, such as attaching the tract ID to each bus stop, crash, signal, employer, or development point. This does not automatically aggregate results to tract level. |
| `find_nearest_feature(source_gdf, target_gdf, distance_column="distance", max_distance=None, projected_epsg=None, how="left")` | Finds the nearest target feature for each source feature and adds a distance column. | Use for questions like nearest rail station to each employer, nearest road segment to each crash, or nearest transit stop to each development. |
| `add_nearest_distance(source_gdf, target_gdf, distance_column="nearest_distance", target_columns=None, unit="meters", projected_epsg=None, source_geometry="geometry")` | Adds only the nearest distance and optional selected target columns. | Use for clean feature engineering, such as tract-centroid distance to rail, nearest major road, nearest employment center, nearest freeway ramp, or nearest hospital. |
| `attach_nearest_features(source_gdf, targets, projected_epsg=None, unit="meters", source_geometry="geometry")` | Adds nearest-distance variables from several target layers in one call. | Use when enriching the same tract, road, or intersection table with multiple proximity measures such as nearest rail, nearest major road, nearest signal, and nearest TMC count. |

Example:

```python
from helper.spatial import spatial_join, find_nearest_feature, add_nearest_distance, attach_nearest_features

bus_stops_with_tract = spatial_join(bus_stops, tracts, predicate="within")
employers_nearest_station = find_nearest_feature(employers, stations, projected_epsg=2276)
tracts = add_nearest_distance(
    tracts,
    stations,
    distance_column="distance_to_nearest_station_miles",
    unit="miles",
    projected_epsg=2276,
    source_geometry="centroid",
)

tracts = attach_nearest_features(
    tracts,
    {"rail_station": stations, "major_road": major_roads},
    unit="miles",
    projected_epsg=2276,
    source_geometry="centroid",
)
```

### Summarizing Points, Lines, and Polygons by Tract

These are the best functions for creating tract-level variables from other
spatial layers.

| Function | What it does | When students should use it |
| --- | --- | --- |
| `summarize_points_by_polygon(polygon_gdf, point_gdf, count_column="point_count", sum_columns=None, predicate="within")` | Counts points inside each polygon and can also sum point attributes. | Use to count bus stops by tract, count development projects by tract, count employers by tract, sum employees by tract, or sum apartment units by tract. |
| `summarize_lines_by_polygon(polygon_gdf, line_gdf, length_column="line_length", count_column="line_count", unit="meters", projected_epsg=None)` | Calculates total line length inside each polygon and optionally counts overlapping line features. | Use to calculate miles of roads, trails, bikeways, bus routes, truck restrictions, or links inside each tract. |
| `summarize_polygons_by_polygon(polygon_gdf, overlap_gdf, area_column="overlap_area", count_column="polygon_count", category_column=None, category_area_prefix=None, unit="square_meters", projected_epsg=None)` | Calculates total polygon overlap area inside each polygon and can create separate area columns by category. | Use to calculate acres of parks inside each tract, area of on-demand transit zones inside each tract, or land-use area by category inside each tract. |

Example:

```python
from helper.spatial import (
    summarize_points_by_polygon,
    summarize_lines_by_polygon,
    summarize_polygons_by_polygon,
)

tracts = summarize_points_by_polygon(
    tracts,
    bus_stops,
    count_column="bus_stop_count",
)

tracts = summarize_points_by_polygon(
    tracts,
    employers,
    count_column="employer_count",
    sum_columns={"EMPLOYEES": "total_employees"},
)

tracts = summarize_lines_by_polygon(
    tracts,
    bikeways,
    length_column="bikeway_miles",
    unit="miles",
    projected_epsg=2276,
)

tracts = summarize_polygons_by_polygon(
    tracts,
    parks,
    area_column="park_acres",
    unit="acres",
    projected_epsg=2276,
)
```

### Accessibility, Coverage, and Connectivity Summaries

Use these when students need the section 4 variables that require extra
spatial aggregation: proximity, nearby opportunities, facility coverage,
street connectivity, major-road access, and land-use context.

| Function | What it does | When students should use it |
| --- | --- | --- |
| `summarize_points_within_distance(source_gdf, point_gdf, distance, count_column="nearby_point_count", sum_columns=None, projected_epsg=None, source_geometry="geometry")` | Counts and sums point features within a buffer around each source feature. | Use for jobs within three miles, transit stops within a half mile, crashes near a road, signals near an intersection, or destinations near tract centroids. |
| `summarize_lines_within_distance(source_gdf, line_gdf, distance, length_column="nearby_line_length", unit="meters", projected_epsg=None, source_geometry="geometry")` | Measures line length within a buffer around each source feature. | Use for major-road access, bikeway coverage near intersections, bus-route miles near neighborhoods, freight-corridor exposure, or trails near tracts. |
| `summarize_polygons_within_distance(source_gdf, polygon_gdf, distance, area_column="nearby_polygon_area", category_column=None, unit="square_meters", projected_epsg=None, source_geometry="geometry")` | Measures polygon area within a buffer around each source feature and can split area by category. | Use for nearby commercial land use, parks, service zones, airport influence, development areas, or land-use context around intersections. |
| `calculate_facility_coverage(polygon_gdf, facility_gdf, buffer_distance, coverage_area_column="facility_coverage_area", coverage_percent_column="facility_coverage_percent", unit="square_meters", projected_epsg=None)` | Calculates the area and percent of each polygon covered by facility buffers, without double-counting overlapping buffers. | Use for percent of a tract within walking distance of transit stops, parks, trails, bikeways, rail stations, EV chargers, schools, or medical facilities. |
| `summarize_street_connectivity(polygon_gdf, road_gdf, projected_epsg=None, ...)` | Creates approximate road length, road density, node count, intersection count, dead-end count, intersection density, links per node, and average segment length. | Use for street connectivity, roadway density, intersection density, intersection spacing, and local-network context. |

Example:

```python
from helper.spatial import (
    summarize_points_within_distance,
    summarize_lines_within_distance,
    calculate_facility_coverage,
    summarize_street_connectivity,
)

tracts = summarize_points_within_distance(
    tracts,
    employers,
    distance=5280 * 3,
    sum_columns={"EMPLOYEES": "jobs_within_3_miles"},
    projected_epsg=2276,
    source_geometry="centroid",
)

intersections = summarize_lines_within_distance(
    intersections,
    bikeways,
    distance=1320,
    length_column="bikeway_miles_within_quarter_mile",
    unit="miles",
    projected_epsg=2276,
)

tracts = calculate_facility_coverage(
    tracts,
    bus_stops,
    buffer_distance=2640,
    coverage_area_column="transit_access_acres",
    coverage_percent_column="pct_tract_near_transit",
    unit="acres",
    projected_epsg=2276,
)

tracts = summarize_street_connectivity(tracts, roads, projected_epsg=2276)
```

### Assigning One Best Polygon by Maximum Overlap

Use these when a feature touches more than one tract or category polygon, but
students need one final label.

| Function | What it does | When students should use it |
| --- | --- | --- |
| `assign_lines_by_max_overlap(line_gdf, polygon_gdf, polygon_columns=None, overlap_length_column="overlap_length", overlap_fraction_column="overlap_fraction", unit="meters", projected_epsg=None, polygon_prefix="")` | Assigns each line to the polygon containing the largest length of that line. | Use when links, roads, routes, trails, or other line features cross tract boundaries and each line needs one tract label. For example, a link that is 80 percent in one tract and 20 percent in another will be assigned to the 80 percent tract. |
| `assign_polygons_by_max_overlap(polygon_gdf, overlap_gdf, overlap_columns=None, overlap_area_column="overlap_area", overlap_fraction_column="overlap_fraction", unit="square_meters", projected_epsg=None, overlap_prefix="")` | Assigns each polygon to the overlapping polygon that covers the largest area. | Use when tracts need one dominant label from a larger polygon layer, such as congestion severity, service zone, transit-on-demand zone, or other area classification. |

Example:

```python
from helper.spatial import assign_lines_by_max_overlap, assign_polygons_by_max_overlap

links_with_tract = assign_lines_by_max_overlap(
    links,
    tracts,
    polygon_columns=["GEOID"],
    unit="meters",
    projected_epsg=2276,
)

tracts_with_congestion = assign_polygons_by_max_overlap(
    tracts,
    congestion,
    overlap_columns=["severity"],
    unit="acres",
    projected_epsg=2276,
)
```

### Clipping, Mapping, and Saving

| Function | What it does | When students should use it |
| --- | --- | --- |
| `clip_to_boundary(gdf, boundary_gdf)` | Keeps only features that intersect a boundary dataset. | Use to limit roads, stops, parks, or other features to a study area such as Dallas County, a city, a corridor, or selected tracts. |
| `quick_plot(gdf, column=None, figsize=(10, 8), legend=True, **kwargs)` | Creates a simple static map from a GeoDataFrame. | Use in notebooks to quickly check whether data loaded correctly, whether geometry locations look reasonable, or how a variable varies across space. |
| `save_gdf(gdf, output_path, driver=None, **kwargs)` | Saves a GeoDataFrame as GeoJSON, GeoPackage, or Shapefile. | Use after cleaning, joining, summarizing, or measuring data so the result can be reused in another notebook, GIS software, or a web map. |

Example:

```python
from helper.spatial import clip_to_boundary, quick_plot, save_gdf

roads_in_tracts = clip_to_boundary(roads, tracts)
ax = quick_plot(tracts, column="bus_stop_count", cmap="Blues")
save_gdf(tracts, "outputs/tract_summary.geojson")
```

## `helper/visualization`

Use these functions to make maps from GeoPandas GeoDataFrames. They work with
point, line, and polygon shapefiles and can color features by data values or
categories.

### Single-Layer Maps

| Function | What it does | When students should use it |
| --- | --- | --- |
| `plot_polygons(gdf, column=None, color="lightgray", cmap="Reds", ...)` | Draws polygon features and can shade them by a data column. | Use for tracts, parks, land-use polygons, congestion zones, service areas, airports, or other polygon layers. |
| `plot_choropleth(gdf, column, cmap="Reds", ...)` | Draws a shaded polygon map from light to dark using a numeric column. | Use for tract-level values such as total employers, population, income, bus stop count, crash count, park acres, or apartment units. |
| `plot_points(gdf, column=None, color="black", cmap="viridis", ...)` | Draws point features and can color them by a data column. | Use for bus stops, employers, developments, crashes, rail stations, EV stations, signals, signs, or other point layers. |
| `plot_lines(gdf, column=None, color="black", cmap="viridis", ...)` | Draws line features and can color them by a data column. | Use for roads, links, bus routes, trails, bikeways, truck restrictions, speed-limit segments, or other line layers. |
| `plot_categorical_map(gdf, column, cmap="tab20", ...)` | Gives each category in a column a different color. | Use for congestion severity, land-use type, development status, road class, facility type, or transit zone name. |
| `plot_graduated_points(gdf, size_column, color_column=None, ...)` | Draws points with marker sizes scaled by a numeric value. | Use when larger points should represent larger employers, more apartment units, larger development projects, crash counts, or station activity. |

Example:

```python
from helper.visualization import plot_choropleth, plot_graduated_points

ax = plot_choropleth(
    tracts,
    column="total_employees",
    cmap="Reds",
    title="Total Employers by Census Tract",
)

ax = plot_graduated_points(
    employers,
    size_column="EMPLOYEES",
    color_column="EMPLOYEES",
    cmap="OrRd",
    title="Employer Size",
)
```

### Multi-Layer and Comparison Maps

| Function | What it does | When students should use it |
| --- | --- | --- |
| `plot_layers(layers, title=None, ...)` | Draws multiple GeoDataFrames on the same map. | Use to overlay tracts, bus routes, bus stops, roads, parks, development points, or any other combination of point, line, and polygon layers. |
| `plot_before_after(before_gdf, after_gdf, before_column=None, after_column=None, ...)` | Draws two maps side by side. | Use to compare raw vs joined data, before vs after filtering, current vs future scenarios, or two different variables. |
| `add_basemap_context(ax, boundary_gdf=None, title=None, ...)` | Cleans up the map frame and can zoom to a boundary layer. | Use after plotting when students want a clean map with no axes, equal map scale, a title, and a useful extent. This does not download web basemap tiles. |
| `save_map(fig, output_path, dpi=300, ...)` | Saves a map as `.png`, `.jpg`, `.jpeg`, `.pdf`, or `.svg`. | Use when students need to include a map in a report, presentation, or project output folder. |

Example:

```python
from helper.visualization import plot_layers, save_map

ax = plot_layers(
    [
        {"gdf": tracts, "type": "polygon", "column": "total_employees", "cmap": "Reds"},
        {"gdf": bus_routes, "type": "line", "color": "blue", "linewidth": 1},
        {"gdf": bus_stops, "type": "point", "color": "black", "markersize": 8},
    ],
    title="Transit Access and Employment",
)

save_map(ax.figure, "outputs/transit_access_employment.png")
```

## `helper/ml`

Use these functions after students have created an analysis table, usually one
row per Census tract, corridor, link, employer, development project, or crash
location. These helpers use `scikit-learn`, so students should install the
project requirements before using them.

### Preparing Data

| Function | What it does | When students should use it |
| --- | --- | --- |
| `prepare_ml_data(df, feature_columns, target_column=None, ...)` | Selects model features, handles missing feature values, scales numeric columns, and converts categorical columns into numeric dummy variables. | Use before clustering, PCA, regression, or classification. This is the main bridge from a cleaned analysis table to machine learning. |
| `split_train_test(data, y=None, target_column=None, ...)` | Splits features and target values into training and testing sets. | Use before regression or classification so students can evaluate models on data that was not used for training. |

Example:

```python
from helper.ml import prepare_ml_data, split_train_test

features = ["population", "bus_stop_count", "total_employees", "park_acres"]

ml_data = prepare_ml_data(
    tracts,
    feature_columns=features,
    target_column="crash_count",
)

split_data = split_train_test(ml_data, test_size=0.2, random_state=42)
```

### Clustering and Pattern Discovery

| Function | What it does | When students should use it |
| --- | --- | --- |
| `run_kmeans_clustering(data, n_clusters=4, ...)` | Groups records into a fixed number of clusters. | Use to group similar tracts by demographics, land use, employment, transit access, safety, congestion, or other numeric features. |
| `find_best_k_for_kmeans(data, k_values=range(2, 11), ...)` | Tests several K-Means cluster counts and reports inertia and silhouette score. | Use before final K-Means clustering to choose a reasonable number of clusters. |
| `run_dbscan_clustering(data, eps=0.5, min_samples=5, ...)` | Finds dense clusters and labels outliers as `-1`. | Use when students want to detect unusual records, dense development/employment patterns, or outlier tracts. |
| `run_hierarchical_clustering(data, n_clusters=4, ...)` | Groups records with agglomerative hierarchical clustering. | Use for smaller datasets where students want an interpretable grouping method. |
| `run_gaussian_mixture_clustering(data, n_components=4, ...)` | Creates probabilistic clusters and membership probabilities. | Use when students want softer cluster assignments instead of only one hard grouping. |
| `evaluate_clustering(data, labels)` | Calculates cluster counts and clustering quality metrics. | Use after clustering to understand whether the groups are separated and how many records are in each cluster. |
| `summarize_clusters(df, cluster_column="cluster", ...)` | Summarizes average feature values by cluster. | Use to explain what each cluster means, such as high employment and low transit access. |
| `run_pca(data, n_components=2, ...)` | Reduces many numeric features into principal components. | Use to simplify many related variables, visualize patterns, or create inputs for clustering. |

Example:

```python
from helper.ml import (
    find_best_k_for_kmeans,
    run_kmeans_clustering,
    evaluate_clustering,
    summarize_clusters,
)

k_scores = find_best_k_for_kmeans(ml_data, k_values=range(2, 8))
cluster_result = run_kmeans_clustering(ml_data, n_clusters=4)

tracts["cluster"] = cluster_result["labels"]
cluster_metrics = evaluate_clustering(ml_data, cluster_result["labels"])
cluster_summary = summarize_clusters(tracts, cluster_column="cluster")
```

### Regression Models

| Function | What it does | When students should use it |
| --- | --- | --- |
| `run_regression_model(X_train, y_train=None, X_test=None, model_type="random_forest", ...)` | Trains one regression model and optionally predicts test values. | Use to predict numeric outcomes such as crash counts, traffic volume, average speed, ridership, employment, or development units. |
| `compare_regression_models(X_train, y_train=None, X_test=None, y_test=None, ...)` | Trains several regression models and compares MAE, MSE, RMSE, and R2. | Use when students want to compare linear regression, ridge, lasso, decision tree, random forest, and gradient boosting. |
| `compare_models(X_train, y_train=None, X_test=None, y_test=None, task_type="auto", ...)` | Compares a broader set of supervised models, including a baseline, linear/logistic models, trees, random forest, extra trees, gradient boosting, histogram gradient boosting, KNN, and SVM where appropriate. | Use when students should spend more time on AI model selection and compare whether more complex models improve over a simple baseline. |
| `evaluate_regression(y_true, y_pred)` | Calculates regression accuracy metrics. | Use after making numeric predictions to understand model error. |

Example:

```python
from helper.ml import compare_models, compare_regression_models, run_regression_model, evaluate_regression

comparison = compare_regression_models(split_data)
broader_comparison = compare_models(split_data, task_type="regression")
best_result = run_regression_model(split_data, model_type="random_forest")
metrics = evaluate_regression(best_result["y_test"], best_result["predictions"])
```

### Classification Models

| Function | What it does | When students should use it |
| --- | --- | --- |
| `run_classification_model(X_train, y_train=None, X_test=None, model_type="random_forest", ...)` | Trains one classification model and optionally predicts test classes. | Use to predict categories such as high/medium/low crash risk, congestion class, transit access class, or priority tract status. |
| `compare_classification_models(X_train, y_train=None, X_test=None, y_test=None, ...)` | Trains several classifiers and compares accuracy, precision, recall, F1, and ROC-AUC when available. | Use when students want to compare logistic regression, decision tree, random forest, gradient boosting, KNN, and SVM. |
| `compare_models(X_train, y_train=None, X_test=None, y_test=None, task_type="auto", ...)` | Compares a broader set of supervised models and returns sorted metrics, fitted models, predictions, probabilities, and model errors if any model fails. | Use for both regression and classification when students want one consistent model-comparison workflow. |
| `evaluate_classification(y_true, y_pred, y_prob=None, labels=None)` | Calculates classification metrics, confusion matrix, and classification report. | Use after class predictions to see which classes the model predicts well or poorly. |

Example:

```python
from helper.ml import compare_classification_models, compare_models, run_classification_model

classification_data = prepare_ml_data(
    tracts,
    feature_columns=features,
    target_column="high_crash_risk",
)

split_data = split_train_test(classification_data, stratify="y")
comparison = compare_classification_models(split_data)
broader_comparison = compare_models(split_data, task_type="classification")
model_result = run_classification_model(split_data, model_type="random_forest")
```

### Model Interpretation and Prediction

| Function | What it does | When students should use it |
| --- | --- | --- |
| `get_feature_importance(model, feature_names=None, top_n=None)` | Extracts feature importance from tree models or coefficients from linear/logistic models. | Use after model training to explain which variables helped the prediction most. |
| `explain_model_results(model, X, y=None, task_type="auto", ...)` | Returns a student-friendly explanation bundle with metrics, feature importance, optional permutation importance, predictions, and largest errors or misclassified records. | Use after choosing a model so students can connect AI output back to transportation meaning instead of reporting accuracy alone. |
| `predict_with_model(model, X, output_column="prediction", ...)` | Applies a fitted model to new data and returns predictions. | Use to predict all tracts, a future scenario, or a cleaned table that was not part of training. |

Example:

```python
from helper.ml import explain_model_results, get_feature_importance, predict_with_model

importance = get_feature_importance(
    model_result["model"],
    feature_names=classification_data["X"].columns,
)

explanation = explain_model_results(
    model_result["model"],
    model_result["X_test"],
    model_result["y_test"],
    task_type="classification",
)

predicted = predict_with_model(model_result["model"], classification_data["X"])
```

## `helper/eda`

Use these functions during exploratory data analysis. They help students
understand the table before making maps, calculating features, or running ML.

| Function | What it does | When students should use it |
| --- | --- | --- |
| `summarize_columns(df)` | Summarizes data type, missing values, unique values, and an example value for every column. | Use after reading or joining a dataset to understand what columns are available. |
| `missing_value_summary(df, only_missing=True)` | Reports missing value counts and percentages. | Use before cleaning, feature engineering, or ML. |
| `numeric_summary(df, columns=None)` | Gives summary statistics for numeric columns. | Use for variables such as population, crashes, traffic volume, speed, income, or employment. |
| `categorical_summary(df, columns=None, top_n=10)` | Counts common values in categorical columns. | Use for road class, congestion severity, development status, land-use type, or crash severity. |
| `correlation_table(df, columns=None, method="pearson")` | Returns pairwise numeric correlations in a sortable table. | Use to identify possible relationships before regression or classification. |
| `compare_groups(df, group_column, value_columns, ...)` | Compares numeric values across groups. | Use after creating clusters, crash groups, congestion classes, or road classes. |
| `find_outliers(df, columns=None, method="iqr")` | Flags unusual numeric values. | Use to find unusual tracts, roads, intersections, or crash records. |
| `create_quantile_groups(df, column, q=4, labels=None)` | Creates equal-sized groups from a numeric column. | Use to create low/medium/high or quartile groups for mapping or classification. |

Example:

```python
from helper.eda import summarize_columns, correlation_table, compare_groups

summary = summarize_columns(tracts)
correlations = correlation_table(tracts, ["crash_count", "population", "bus_stop_count"])
cluster_comparison = compare_groups(tracts, "cluster", ["crash_count", "total_employees"])
```

## `helper/features`

Use these functions to create analysis-ready variables. These helpers are often
used after spatial joins and before similarity analysis or ML.

| Function | What it does | When students should use it |
| --- | --- | --- |
| `create_rate(df, numerator, denominator, output_column, multiplier=1.0)` | Creates a rate from two columns. | Use for crashes per population, crashes per AADT, stops per mile, or other normalized measures. |
| `create_density(df, value_column, area_column, output_column)` | Creates a density value using an area column. | Use for population density, employer density, crash density, or bus stop density. |
| `create_share(df, part_column, total_column, output_column)` | Creates a share or percentage. | Use for mode share, land-use share, severe crash share, or employment share. |
| `create_binary_flag(df, column, threshold, output_column, operator=">=")` | Creates a 0/1 threshold flag. | Use for high-crash tracts, high-congestion roads, or priority locations. |
| `create_category_from_bins(df, column, bins, labels, output_column)` | Creates categories from numeric ranges. | Use for low/medium/high crash rate, congestion, income, speed, or density classes. |
| `normalize_columns(df, columns, method="zscore")` | Adds normalized numeric columns. | Use before similarity analysis, clustering, PCA, KNN, or SVM. |
| `calculate_difference_from_group_mean(df, group_column, value_column)` | Compares each row with its group average. | Use to find roads or intersections that behave differently from similar peers. |
| `calculate_land_use_mix(df, area_columns, output_column="land_use_mix")` | Calculates an entropy-based diversity index from land-use area columns. | Use after summarizing land-use area by category to represent mixed-use development or land-use diversity. |

Example:

```python
from helper.features import create_rate, create_density, create_binary_flag, calculate_land_use_mix

tracts = create_rate(tracts, "crash_count", "population", "crashes_per_1000_people", multiplier=1000)
tracts = create_density(tracts, "total_employees", "area_sq_miles", "employees_per_sq_mile")
tracts = create_binary_flag(tracts, "crash_count", 20, "high_crash_tract")
tracts = calculate_land_use_mix(
    tracts,
    ["acres_residential", "acres_commercial", "acres_institutional"],
)
```

## `helper/similarity`

Use these functions when the research question asks why similar places, roads,
or intersections have different outcomes.

| Function | What it does | When students should use it |
| --- | --- | --- |
| `calculate_similarity_matrix(df, feature_columns, id_column=None, ...)` | Calculates pairwise similarity or distance between records. | Use to compare all tracts, roads, or intersections based on selected characteristics. |
| `find_similar_records(df, id_column, feature_columns, target_id, n=10)` | Finds the most similar records to one selected record. | Use when students choose one tract, road, or intersection and want peer examples. |
| `find_similar_pairs(df, feature_columns, id_column=None, max_pairs=100)` | Finds the most similar pairs in a dataset. | Use to identify pairs that should behave similarly based on selected inputs. |
| `compare_similar_records(df, feature_columns, outcome_column, ...)` | Finds similar pairs with different outcomes. | Use directly for questions like similar neighborhoods with different travel patterns or similar roads with different congestion. |
| `rank_unexpected_outcomes(df, feature_columns, outcome_column, ...)` | Ranks records whose outcomes differ from their nearest peers. | Use to identify unexpected high-crash tracts, congested roads, or risky intersections. |

Example:

```python
from helper.similarity import compare_similar_records, rank_unexpected_outcomes

similar_but_different = compare_similar_records(
    tracts,
    feature_columns=["income", "population", "education_share"],
    outcome_column="transit_mode_share",
    id_column="GEOID",
)

unexpected_roads = rank_unexpected_outcomes(
    roads,
    feature_columns=["lanes", "speed_limit", "traffic_volume"],
    outcome_column="congestion_index",
    id_column="road_id",
)
```

## `helper/transportation`

Use these functions for transportation-specific summaries and indicators.

| Function | What it does | When students should use it |
| --- | --- | --- |
| `calculate_speed_ratio(df, speed_column, free_flow_column, ...)` | Calculates observed speed divided by free-flow speed. | Use as a simple congestion indicator for roads or links. |
| `classify_congestion(df, speed_ratio_column="speed_ratio", ...)` | Classifies speed ratio as severe, medium, or low congestion. | Use to create a categorical congestion outcome for maps or classification. |
| `calculate_crash_rate(df, crash_column, exposure_column, ...)` | Calculates crashes divided by exposure. | Use for crash rates per population, AADT, VMT, road mile, or intersection volume. |
| `calculate_mode_share(df, group_column, mode_column, weight_column=None)` | Calculates mode counts and shares by group. | Use for origin tracts, destination tracts, demographic groups, or trip purposes. |
| `aggregate_od_flows(od_data, origin_column, destination_column=None, mode_column=None, ...)` | Aggregates detailed OD/trip records by origin, destination, mode, time, or a custom grouping; works with DataFrames or CSV chunk iterators. | Use for Challenge 1 when students need origin-destination summaries without writing chunked groupby code. |
| `summarize_od_by_origin(od_df, origin_column, mode_column=None, ...)` | Summarizes OD/trip records by origin. | Use for Challenge 1 travel patterns by home or origin tract. |
| `summarize_od_by_destination(od_df, destination_column, mode_column=None, ...)` | Summarizes OD/trip records by destination. | Use to identify major destinations and compare destination patterns. |
| `summarize_time_patterns(df, group_column, time_column, time_unit="hour")` | Summarizes records by hour, day of week, month, or weekday/weekend. | Use for trip, traffic, or crash time patterns. |

Example:

```python
from helper.transportation import aggregate_od_flows, calculate_speed_ratio, classify_congestion, calculate_mode_share

roads = calculate_speed_ratio(roads, "avg_speed", "free_flow_speed")
roads = classify_congestion(roads)
mode_share = calculate_mode_share(trips, "origin_trct_2020", "mode")
flows = aggregate_od_flows(
    trips,
    origin_column="origin_trct_2020",
    destination_column="destination_trct_2020",
    mode_column="mode",
)
```

## `helper/safety`

Use these functions for crash and safety analysis, especially Challenges 3 and
4.

| Function | What it does | When students should use it |
| --- | --- | --- |
| `read_txdot_crashes(file_path, header_row="auto", ...)` | Reads TxDOT crash CSV exports, finds the real header row when preamble rows exist, cleans column names, removes duplicate crash IDs, converts coordinates, and can return a GeoDataFrame. | Use before Challenge 3 or 4 crash analysis so students do not need to write custom CSV cleanup code. |
| `summarize_crashes_by_area(crash_gdf, area_gdf, ...)` | Counts crash points inside polygon areas and can count by severity. | Use to create crash counts by tract, zone, or neighborhood. |
| `summarize_crashes_by_road(crash_gdf, road_gdf, buffer_distance, ...)` | Counts crashes within a buffer of each road segment. | Use when crash points need to be associated with nearby road links. |
| `summarize_crashes_by_intersection(crash_gdf, intersection_gdf, buffer_distance, ...)` | Counts crashes within a buffer of each intersection. | Use for intersection safety analysis. |
| `create_crash_severity_summary(df, group_column, severity_column)` | Counts crash severity categories by group. | Use to compare injury, fatal, or property-damage crash patterns. |
| `create_crash_time_summary(crash_df, group_column, time_column, ...)` | Summarizes crashes by time period and group. | Use to compare hourly, monthly, weekday, or weekend crash patterns. |
| `calculate_crash_rate_by_group(df, crash_column, exposure_column, ...)` | Calculates crash rates for grouped data. | Use after joining crash counts with population, AADT, VMT, road length, or entering volume. |

Example:

```python
from helper.safety import read_txdot_crashes, summarize_crashes_by_area, summarize_crashes_by_intersection

crashes = read_txdot_crashes("data/txdot_crashes.csv")
tracts = summarize_crashes_by_area(crashes, tracts, severity_column="severity")
intersections = summarize_crashes_by_intersection(
    crashes,
    intersections,
    buffer_distance=150,
    projected_epsg=2276,
)
```

## Suggested Workflow for Students

1. Read the data with `helper.data_read`; use `read_large_csv_in_chunks` for
   large OD, traffic, TMC, or turning-movement files.
2. Use dataset-specific cleaners such as `read_txdot_crashes` when they match
   the source file.
3. Inspect spatial data with `summarize_gdf` and `check_crs`.
4. Clean, assign CRS, and project spatial data with `prepare_spatial_data`
   before measuring distance, length, or area.
5. Use the right join or summary function:
   - Points to tracts: `summarize_points_by_polygon`
   - Lines to one tract label: `assign_lines_by_max_overlap`
   - Lines summarized by tract: `summarize_lines_by_polygon`
   - Polygons to one dominant tract label: `assign_polygons_by_max_overlap`
   - Polygon areas summarized by tract: `summarize_polygons_by_polygon`
   - Nearby jobs, stops, signals, destinations, or crashes: `summarize_points_within_distance`
   - Nearby major roads, bikeways, trails, routes, or freight corridors: `summarize_lines_within_distance`
   - Nearby land use, parks, zones, or development areas: `summarize_polygons_within_distance`
   - Several nearest-feature distances at once: `attach_nearest_features`
   - Service or facility coverage: `calculate_facility_coverage`
   - Street connectivity: `summarize_street_connectivity`
6. Summarize OD/trip records with `aggregate_od_flows` when detailed trip
   tables need to become analysis-ready flow tables.
7. Explore the joined table with `helper.eda`.
8. Create rates, densities, shares, flags, land-use mix, and categories with
   `helper.features`.
9. Use `helper.similarity` to find similar records and unexpected outcomes.
10. Use `helper.transportation` and `helper.safety` for domain-specific
   indicators and summaries.
11. Map quick checks with `quick_plot`, or make cleaner final maps with
   `helper.visualization`.
12. Save final spatial outputs with `save_gdf`.
13. Save final map images with `save_map`.
14. Prepare an analysis table with `prepare_ml_data`.
15. Use clustering/PCA for pattern discovery, or split the data with
    `split_train_test` before regression or classification.
16. Use `compare_models` to test several algorithms, then use
    `explain_model_results` to interpret metrics, feature importance, and
    errors before presenting results.

## Notes

- Use a projected CRS for distance, length, area, buffers, and overlap
  calculations. For Dallas-area examples, students can often use
  `projected_epsg=2276`.
- `spatial_join` is useful for simple row-by-row joins, but it does not create
  tract-level counts or sums. Use the summary helpers when the goal is one row
  per tract.
- Files beginning with an underscore, such as `_join_helpers.py`, are internal
  support files for the helper package. Students usually do not need to import
  them directly.
- Machine learning helpers require `scikit-learn`. Install the packages in
  `requirements.txt` before running `helper.ml` examples.
