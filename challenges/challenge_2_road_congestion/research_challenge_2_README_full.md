# Research Challenge 2
## Why Do Roads with Similar Physical and Traffic Characteristics Experience Different Levels of Congestion?

## 1. Challenge Overview

Road segments with nearly identical physical characteristics—including speed limit, functional classification, number of lanes, and average traffic volume—do not always experience similar congestion. Some corridors operate efficiently throughout the day, while others experience recurring bottlenecks, unstable traffic flow, and significant travel-time variability under what appear to be nearly identical conditions.

This research challenge asks participants to investigate why these differences exist by integrating multiple transportation, land-use, demographic, environmental, and operational datasets for Dallas County. The objective is not merely to predict congestion, but to explain why physically similar roads perform differently and identify the hidden mechanisms responsible for those differences.

A useful research question is:

> After controlling for roadway geometry and traffic demand, which transportation, operational, accessibility, land-use, and environmental factors best explain why some roads become congested while others continue to operate efficiently?

---

## 2. Why This Challenge Matters in Transportation

Traffic congestion is one of the most important and expensive challenges facing modern transportation systems. Congestion increases travel time, fuel consumption, emissions, crash exposure, freight costs, transit unreliability, and economic losses. Metropolitan regions spend billions of dollars every year attempting to reduce congestion through infrastructure expansion, traffic management, intelligent transportation systems, and operational improvements.

Despite decades of research, congestion remains difficult to understand because it is rarely caused by a single factor. Similar roads often experience completely different traffic conditions because congestion emerges from interactions among roadway geometry, travel demand, traffic control, network topology, surrounding land use, incidents, traveler behavior, and temporal variation.

Understanding why similar roads behave differently is important because transportation agencies continuously make decisions regarding:

1. Corridor improvement projects.
2. Signal timing optimization.
3. Congestion mitigation programs.
4. Freight movement.
5. Transit priority.
6. Incident management.
7. Intelligent Transportation Systems (ITS).
8. Long-term infrastructure investment.

Rather than asking whether congestion exists, this challenge asks why congestion appears on one road but not another when both roads initially appear nearly identical.

---

## 3. Why Finding the Answer Is Difficult

Congestion is an emergent property of the transportation network rather than an isolated property of a roadway segment.

Major difficulties include:

### 3.1 Similar roads are rarely truly identical

Roads may have the same speed limit and lane count while differing in intersection spacing, driveway density, surrounding land use, or downstream bottlenecks.

### 3.2 Congestion is dynamic

Traffic conditions change continuously throughout the day. A road may operate well during off-peak periods but become unstable during the morning or evening peak.

### 3.3 Congestion propagates

Traffic queues travel upstream through the network. A downstream bottleneck may create congestion several miles away from the actual cause.

### 3.4 Multiple mechanisms create congestion

Congestion may result from:
- insufficient capacity,
- signal timing,
- lane drops,
- heavy turning movements,
- incidents,
- weather,
- construction,
- freight operations,
- poor access management,
- recurring commuter demand.

Different mechanisms can produce similar congestion patterns.

### 3.5 Spatial dependency

Roads cannot be analyzed independently. Every segment interacts with neighboring intersections, arterials, freeways, and local streets.

### 3.6 Association is not causation

Machine-learning models may discover that high employment density is associated with congestion. This does not necessarily imply employment density causes congestion. Additional factors such as transit availability, land use, and network structure may also contribute.

### 3.7 Important operational variables are often unavailable

Many of the variables that transportation engineers would ideally analyze—including signal timing plans, adaptive signal control logs, detector occupancy, queue lengths, and connected vehicle trajectories—are unavailable in most public datasets.

---

## 4. Measurable Structural Factors and Hidden Factors

Congestion is better understood by separating measurable structural variables from latent or difficult-to-observe influences.

### 4.1 Measurable structural factors

Roadway characteristics

- speed limit
- number of lanes
- functional class
- median type
- access density
- intersection spacing
- roadway curvature
- roadway connectivity

Traffic characteristics

- AADT
- hourly traffic volume
- average speed
- median speed
- free-flow speed
- travel time index
- congestion index

Transportation system characteristics

- signal density
- transit routes
- transit stops
- freight corridors
- bicycle infrastructure
- nearby parking
- incident frequency
- crash density

Land-use and accessibility

- employment density
- population density
- commercial activity
- destination density
- jobs-housing balance
- accessibility to major activity centers
- network centrality

Environmental

- weather
- construction
- work zones
- seasonal effects
- time of day
- day of week

These variables influence congestion but do not deterministically create it.

### 4.2 Hidden or difficult-to-observe factors

- driver behavior
- route choice
- navigation applications
- adaptive signal coordination
- parking search
- delivery operations
- special events
- queue spillback
- temporary lane blockage
- traveler familiarity
- work schedule flexibility
- traffic management strategies
- connected vehicle behavior

These variables should be recognized as possible explanations even when they cannot be measured directly.

### 4.3 Helper functions that support measurable factors

Several congestion-related structural variables can be created with helper functions:

- `summarize_street_connectivity` for roadway density, intersection density, roadway connectivity, dead ends, links per node, and average segment length;
- `summarize_lines_within_distance` for nearby major roads, freight corridors, bus routes, bikeways, and construction or work-zone line exposure;
- `summarize_points_within_distance` for signal density, transit-stop density, crash density, incident frequency, employers, and destinations near a road segment;
- `summarize_polygons_within_distance` for nearby commercial activity, employment areas, development areas, service zones, and land-use context;
- `add_nearest_distance` for proximity to major activity centers, freeway ramps, rail stations, or other network anchors;
- `calculate_facility_coverage` for service or infrastructure coverage around corridors or nearby neighborhoods; and
- `calculate_land_use_mix` for land-use diversity after land-use area has been summarized by category.

---

## 5. How to Think About the Problem

The project should be approached as a controlled comparison rather than a countywide congestion prediction problem.

### Step 1: Define roadway similarity

Representative variables include:

- speed limit
- number of lanes
- functional class
- AADT
- roadway type

Standardize these variables before calculating similarity.

Similarity may be determined using nearest neighbors, Euclidean distance, cosine similarity, clustering, or matching techniques.

### Step 2: Define congestion

Representative congestion measures include:

- average speed reduction
- speed ratio
- travel time index
- congestion index
- average delay

Choose one primary congestion measure.

### Step 3: Identify contrasting road pairs

Road pairs should satisfy two conditions:

1. physically similar;
2. substantially different congestion.

### Step 4: Build explanatory variables

Possible variables include:

- intersection density
- signal density
- incident frequency
- crash density
- transit accessibility
- nearby employment
- nearby population
- land-use diversity
- freight activity
- construction
- weather
- network connectivity

### Step 5: Compare and model

Begin with visualization before applying machine learning.

Representative models include:

- linear regression
- decision trees
- random forest
- gradient boosting

Explainability methods such as SHAP and permutation importance should support transportation reasoning rather than replace it.

### Step 6: Evaluate alternative explanations

Questions include:

- Is the factor consistent across multiple corridors?
- Does it make transportation sense?
- Is another correlated variable responsible?
- Could missing operational variables explain the difference?

### Step 7: Produce an evidence-based explanation

A strong conclusion should rank explanatory factors while acknowledging uncertainty and avoiding unsupported causal claims.

---

## 6. Data That Can Help Answer the Challenge

### Available datasets

Transportation infrastructure

- roadway inventory
- functional class
- speed limits
- lane counts
- intersections
- signals

Traffic

- AADT
- hourly volumes
- average hourly speed
- median speed
- free-flow speed

Operations

- incidents
- crashes
- construction

Mobility

- Replica OD
- trip purpose
- trip timing

Transit

- routes
- stops

GIS

- network
- land use
- points of interest
- accessibility indicators

Demographics

- Census
- employment
- income
- population
- commuting

Environment

- weather

### Important missing datasets

- signal timing plans
- adaptive signal controller data
- queue lengths
- detector occupancy
- connected vehicle trajectories
- lane-by-lane volumes
- parking activity
- delivery operations
- navigation app routing
- detailed freight schedules

---

## 7. Where Does AI and Machine Learning Fit?

Artificial Intelligence is not the objective of this challenge. The transportation question remains the same: why do physically similar roads experience different congestion? AI provides analytical tools for discovering relationships that traditional statistical analysis may overlook.

AI contributes by:

- discovering similar roadway segments,
- integrating heterogeneous datasets,
- predicting congestion,
- identifying nonlinear interactions,
- explaining important variables,
- generating new hypotheses.

### Possible AI/ML Methods

| Complexity | Methods | Role |
|---|---|---|
| Very Simple | Correlation, PCA, K-Means | Explore data and identify similar roads |
| Simple | Linear Regression | Baseline interpretable model |
| Moderate | Decision Trees, Random Forest | Capture nonlinear relationships |
| Moderate-Advanced | XGBoost, LightGBM, CatBoost | Improve prediction and interaction discovery |
| Advanced | Support Vector Machines | Complex nonlinear prediction |
| Time-Series | LSTM, Temporal CNN | Forecast congestion over time |
| Spatial AI | Graph Neural Networks | Model network interactions |
| Explainable AI | SHAP, LIME, PDP | Explain predictions |
| Causal AI | Causal Forests, Double ML | Estimate intervention effects |

The recommended workflow begins with an interpretable baseline model followed by a tree-based model and explainable AI techniques. The emphasis remains on transportation insight rather than predictive accuracy.

---

## 8. Recommended Analytical Workflow

1. Define roadway similarity.
2. Select one congestion metric.
3. Match similar roadway segments.
4. Compare surrounding transportation environments.
5. Engineer explanatory variables.
6. Train baseline and AI models.
7. Explain results using feature importance or SHAP.
8. Validate across multiple roadway pairs.
9. Translate findings into planning recommendations.

---

## 9. Two Recent Research Papers

### Paper 1

Recent explainable machine-learning research using XGBoost and SHAP for urban congestion prediction demonstrates that congestion can be predicted while simultaneously identifying the variables contributing most strongly to congestion.

The authors framed congestion as both a prediction and interpretation problem. Rather than maximizing predictive accuracy alone, they used explainable AI to rank roadway, operational, environmental, and temporal variables.

Research gap:
Previous studies frequently produced accurate predictions without providing interpretable explanations.

Future work:
Integrate richer traffic operations data, connected vehicles, and causal inference methods.

Relevance:
This study illustrates how explainable AI can identify hidden congestion drivers while supporting engineering interpretation.

### Paper 2

Recent graph neural network research models congestion as a spatio-temporal network process.

The authors represent roads as nodes connected through transportation topology, allowing congestion to propagate naturally through the graph.

Research gap:
Traditional models often ignore spatial dependence between neighboring roads.

Future work:
Improve interpretability, scalability, and real-time deployment.

Relevance:
This work reinforces the systems perspective adopted throughout this challenge.

---

## 10. How the Answer Can Improve Transportation Systems

The findings can help transportation agencies:

- identify hidden bottlenecks,
- prioritize corridor improvements,
- optimize signal timing,
- improve freight mobility,
- improve transit operations,
- reduce emissions,
- reduce travel time,
- improve Digital Twins,
- support resilient transportation systems.

The objective is to produce evidence-based explanations that support engineering and planning decisions.

---

## 11. Expected Final Program Outcome

A successful project should include:

1. reproducible roadway similarity definition;
2. one congestion metric;
3. several matched roadway comparisons;
4. integration of at least four datasets;
5. maps and visualizations;
6. one baseline model;
7. one interpretable machine-learning model;
8. feature-importance analysis;
9. discussion of uncertainty and missing variables; and
10. practical transportation recommendations.

### Example conclusion

> The analysis identified multiple roadway pairs with similar physical characteristics but substantially different congestion. After integrating roadway, demographic, accessibility, operational, and environmental datasets, explainable machine-learning models consistently identified intersection density, access density, nearby employment, incident frequency, and network connectivity as the strongest explanatory factors. These findings suggest that congestion is driven primarily by network context and operational conditions rather than roadway geometry alone. Although causal relationships cannot be established using the available datasets, the results indicate that operational improvements may provide greater benefits than roadway expansion in many corridors.

---

## 12. Minimum Scope

The minimum project includes:

- roadway similarity matching,
- one congestion metric,
- three to five roadway pairs,
- four integrated datasets,
- one baseline model,
- one AI model,
- explainable AI,
- maps,
- limitations,
- actionable recommendations.

The emphasis should remain on reproducible analysis, defensible reasoning, and transportation insight.
