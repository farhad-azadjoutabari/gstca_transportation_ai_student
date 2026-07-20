# Research Challenge 1  
## Why Do Demographically Similar Neighborhoods Exhibit Different Travel Patterns?

## 1. Challenge Overview

Neighborhoods with similar demographic characteristics—such as population, age distribution, household income, educational attainment, employment status, and vehicle ownership—do not necessarily generate similar travel behavior. Two neighborhoods may appear comparable in Census data, yet residents of one neighborhood may drive for most trips while residents of the other use transit more frequently, make shorter trips, travel at different times, or generate different proportions of work, shopping, school, and recreational trips.

This research challenge asks students to investigate the factors that may explain these differences across Dallas County. The central idea is that demographics describe only part of the travel-behavior system. Travel is also influenced by where opportunities are located, how transportation networks are designed, how accessible different modes are, and how people perceive the available choices.

The objective is therefore not merely to predict travel patterns. The objective is to identify demographically similar neighborhoods with meaningfully different travel outcomes, investigate the hidden structural and contextual factors separating them, and evaluate how strongly the available evidence supports the proposed explanations.

A useful research question is:

> After controlling for major demographic characteristics, which transportation, accessibility, land-use, and environmental factors best explain differences in neighborhood travel patterns?

---

## 2. Why This Challenge Matters in Transportation

Transportation agencies frequently use demographic and socioeconomic variables to estimate trip generation, mode choice, and travel demand. These variables are important, but treating demographically similar communities as behaviorally equivalent can produce misleading conclusions.

Understanding the differences matters for several reasons:

1. **Transportation investments should respond to actual constraints.**  
   A neighborhood may have low transit use not because residents prefer driving, but because transit service is infrequent, stops are difficult to reach, or destinations are poorly connected.

2. **Demographic similarity does not imply equal accessibility.**  
   Two households with similar incomes and vehicle ownership may face very different travel choices depending on job proximity, road connectivity, transit coverage, sidewalk conditions, and destination availability.

3. **Planning based only on average relationships can conceal local inequalities.**  
   Countywide models may conclude that income or vehicle ownership explains most automobile use, while overlooking neighborhoods where the built environment or service quality produces unusual outcomes.

4. **Policies must be geographically targeted.**  
   Adding transit service, improving pedestrian infrastructure, changing land use, or managing parking will not have the same effect everywhere. The relevant intervention depends on the mechanism producing the observed travel behavior.

5. **The challenge connects transportation behavior to sustainability and equity.**  
   Explaining why some neighborhoods depend more heavily on automobiles can help agencies identify where realistic alternatives are missing and where infrastructure improvements may reduce travel burden, emissions, and transportation costs.

---

## 3. Why Finding the Answer Is Difficult

Travel behavior is produced by a complex interaction among people, transportation systems, land use, time, and individual decision-making. Several difficulties make the problem challenging.

### 3.1 Similarity is not absolute

Neighborhoods can be similar in income but different in age, household composition, employment, or vehicle ownership. The analysis must define which demographic features establish similarity and decide how close two neighborhoods must be before they are treated as comparable.

### 3.2 Travel behavior has multiple dimensions

“Different travel patterns” may refer to:

- total trips generated;
- average trip distance;
- average travel time;
- share of trips made by automobile, transit, walking, or cycling;
- work versus non-work trips;
- departure-time distributions;
- internal versus external trips;
- weekday versus weekend travel; or
- spatial distribution of destinations.

A pair of neighborhoods may be similar in one outcome but different in another. The research must therefore define one or two primary outcome measures.

### 3.3 Many relationships are nonlinear

Adding one transit stop does not automatically change mode choice. Transit accessibility may begin to matter only after a minimum service density, frequency, or destination coverage is reached. Similar threshold effects can occur for intersection density, employment accessibility, land-use diversity, and distance to major activity centers.

### 3.4 Spatial aggregation can distort relationships

Census tracts are convenient analytical units, but they are not necessarily true neighborhoods or travel markets. Results may change when data are aggregated by tract, block group, grid, or transportation analysis zone. This is part of the Modifiable Areal Unit Problem.

### 3.5 Association is not causation

A machine-learning model may show that transit-stop density is associated with lower automobile use, but it cannot by itself prove that adding transit stops will cause residents to drive less. Transit agencies may already provide more service in locations where transit demand is high. Land use, residential self-selection, and unmeasured preferences may influence both transit availability and travel behavior.

### 3.6 Important behavioral factors are often unavailable

Public datasets describe infrastructure and population characteristics better than they describe attitudes, habits, trip chaining, perceived safety, schedule flexibility, mobility limitations, or reasons for choosing a mode. These unobserved factors can produce different outcomes even when measured neighborhood characteristics appear similar.

---

## 4. Measurable Structural Factors and Non-Deterministic Factors

Travel behavior should not be divided too literally into deterministic and non-deterministic parameters. Very few transportation variables deterministically produce a specific behavior. A better distinction is between measurable structural factors and stochastic, latent, or unobserved factors.

### 4.1 Measurable structural factors

These variables can usually be observed, calculated, or approximated from available datasets.

#### Demographic and socioeconomic factors

- population and household density;
- age distribution;
- income and poverty;
- educational attainment;
- employment status;
- household composition;
- number of workers per household;
- vehicle availability;
- disability status;
- commute mode;
- commute duration; and
- departure time for work.

#### Transportation supply factors

- roadway density;
- functional road class;
- intersection density;
- street connectivity;
- transit-stop density;
- transit-route density;
- proximity to rail or frequent transit;
- accessibility to major roads;
- bicycle-facility coverage;
- congestion and roadway speeds; and
- incident or crash exposure.

#### Land-use and accessibility factors

- distance to employment centers;
- number of reachable jobs;
- proximity to retail, schools, parks, and medical services;
- land-use diversity;
- density of destinations;
- distance to downtown or major activity centers;
- jobs–housing balance; and
- amount of travel remaining within the neighborhood or county.

#### Temporal and environmental factors

- time of day;
- day of week;
- weather;
- school and work schedules;
- recurring congestion; and
- unusual incidents.

These factors are not fully deterministic. They change the probability, convenience, cost, or attractiveness of different travel choices.

### 4.2 Stochastic, behavioral, latent, and difficult-to-observe factors

These factors are real but are often unavailable in open datasets.

- personal mode preference;
- travel habits;
- perceived safety;
- comfort with transit;
- reliability expectations;
- value of time;
- flexible or inflexible work schedules;
- caregiving responsibilities;
- trip chaining;
- parking price and parking availability;
- access to a vehicle at the exact time of travel;
- temporary household circumstances;
- social influence;
- familiarity with available transportation options;
- residential self-selection;
- willingness to walk in heat or bad weather;
- physical mobility limitations not captured in aggregate data; and
- random daily variation.

The analysis should not ignore these variables. They should explicitly identify them as possible explanations that cannot be tested with the available data.

### 4.3 Helper functions that support measurable factors

Several measurable factors listed above can be created with helper functions instead of being coded from scratch:

- `summarize_street_connectivity` for roadway density, intersection density, street connectivity, links per node, dead ends, and average segment length;
- `add_nearest_distance` for distance to rail stations, major roads, employment centers, downtown, parks, schools, medical facilities, or other activity centers;
- `summarize_points_within_distance` for reachable jobs, nearby transit stops, nearby destinations, and nearby services;
- `summarize_lines_within_distance` for major-road access, transit-route density, bicycle-facility mileage, trail mileage, and roadway exposure near a tract or tract centroid;
- `summarize_polygons_within_distance` for nearby land-use area, parks, development areas, or service zones;
- `calculate_facility_coverage` for percent of a tract within walking distance of transit stops, rail stations, bikeways, parks, or other facilities; and
- `calculate_land_use_mix` for land-use diversity after land-use area has been summarized by category.

---

## 5. How to Think About the Problem

The challenge should be approached as a controlled comparison, not as a general countywide prediction exercise.

### Step 1: Define the unit of analysis

The recommended unit is the Census tract because demographic variables are already available at that level. The analysis should recognize that a tract is an analytical proxy for a neighborhood.

### Step 2: Define demographic similarity

Select a small set of variables that represent the demographic profile of each tract. A practical set may include:

- median household income;
- median age or selected age-group shares;
- educational attainment;
- employment rate;
- vehicle availability;
- household size; and
- population density.

Standardize these variables before calculating similarity.

Possible methods include:

- nearest-neighbor matching;
- Euclidean distance after standardization;
- cosine similarity;
- k-means clustering followed by within-cluster comparisons; or
- propensity-score-style matching.

For this project, clustering followed by nearest-neighbor pairing is likely the clearest approach.

### Step 3: Define travel-pattern difference

The analysis should choose one primary outcome and, at most, one secondary outcome.

Representative primary outcomes include:

- automobile commute share;
- transit commute share;
- average commute time;
- total trips per resident;
- average trip distance; or
- proportion of non-work trips.

A useful pair should be close in demographic space but far apart in travel-outcome space.

### Step 4: Identify contrasting neighborhood pairs

The analysis should select several pairs rather than rely on a single example. Each pair should satisfy two conditions:

1. the neighborhoods are demographically similar; and  
2. their selected travel outcomes are substantially different.

### Step 5: Build explanatory features

For each tract, calculate transportation and accessibility variables such as:

- transit stops per square mile;
- transit routes serving the tract;
- road miles per square mile;
- intersection density;
- average roadway speed;
- congestion exposure;
- number of nearby jobs;
- distance to major employment centers;
- destination or point-of-interest density;
- jobs–housing balance;
- crash density;
- incident density; and
- internal versus external trip share.

### Step 6: Compare and model

The analysis should first examine maps, distributions, and pairwise differences. They may then use an interpretable model such as:

- decision tree;
- random forest;
- gradient boosting;
- regularized linear regression; or
- simple classification of “higher-car-use” versus “lower-car-use” neighborhoods.

Feature importance, permutation importance, partial dependence, or SHAP values can help students identify candidate explanations. These tools should support reasoning rather than replace it.

### Step 7: Evaluate alternative explanations

The analysis should ask:

- Is the apparent factor consistent across multiple neighborhood pairs?
- Does the factor make transportation sense?
- Could another correlated variable be responsible?
- Is the relationship likely to be causal, or only associative?
- Could the result be caused by spatial aggregation?
- Which important variables are missing?

### Step 8: Convert findings into a defensible explanation

A strong conclusion should use cautious language, such as:

> Among demographically similar tracts, lower automobile dependence was most consistently associated with higher transit accessibility, greater destination density, and shorter distances to major employment centers. These results suggest that transportation supply and regional accessibility may explain part of the observed difference, although the analysis cannot establish causality or account for individual preferences and parking conditions.

---

## 6. Data That Can Help Answer the Challenge

### 6.1 Available or reasonably obtainable data

The following datasets are available in the project or can be derived from existing project resources.

#### Census and American Community Survey data

- population;
- age;
- income;
- poverty;
- education;
- employment;
- household composition;
- vehicle availability;
- commute mode;
- commute duration;
- departure time;
- occupation;
- industry;
- disability;
- workers by age and sex; and
- place-of-work information.

#### Replica or origin–destination data

- trip origins and destinations;
- trip purpose;
- travel mode;
- trip distance;
- trip duration;
- departure time;
- internal and external trip patterns; and
- destination distribution.

#### Transit data

- transit stops;
- transit routes;
- route coverage;
- distance to nearest stop;
- stop density; and
- approximate network availability.

#### Roadway and traffic data

- roadway network;
- functional classification;
- road density;
- intersection density;
- AADT;
- average and median speed;
- free-flow speed;
- congestion indicators;
- incidents; and
- crashes.

#### OpenStreetMap and GIS-derived variables

- street connectivity;
- intersection type;
- points of interest;
- selected land-use indicators;
- pedestrian-network proxies;
- distance to major roads;
- distance to activity centers; and
- network-based accessibility measures.

#### Weather data

- temperature;
- precipitation;
- severe-weather events; and
- other conditions that may influence active travel or trip timing.

### 6.2 Important data that are missing or difficult to access

The following variables could materially improve the analysis but may not be available within the program.

- individual or household travel-diary records linked directly to demographic attributes;
- real-time transit frequency, reliability, crowding, and missed-service data;
- detailed parking supply and parking prices;
- sidewalk quality and continuity;
- bicycle-lane quality rather than simple presence;
- perceived neighborhood safety;
- perceived transit safety;
- travel attitudes and mode preferences;
- work-from-home frequency at the individual level;
- flexible-work arrangements;
- school assignment and school travel behavior;
- household caregiving and trip-chaining responsibilities;
- ride-hailing use;
- vehicle operating cost perceived by each household;
- longitudinal household behavior;
- parcel-level land use for all of Dallas County;
- precise job accessibility by occupation and skill;
- smartphone or GPS traces with representative demographic coverage; and
- causal evidence showing how behavior changed after a transportation intervention.

The absence of these variables should appear in the limitations section of the final presentation.

---

## 7. Two Recent Research Papers

### Paper 1

**Ashik, F. R., Sreezon, A. I. Z., Rahman, M. H., Zafri, N. M., and Labib, S. M. (2024). “Built Environment Influences Commute Mode Choice in a Global South Megacity Context: Insights from Explainable Machine Learning Approach.” Journal of Transport Geography, 116, 103828. DOI: 10.1016/j.jtrangeo.2024.103828.**

#### How the authors shaped the problem

The authors examined whether built-environment conditions around homes and workplaces help explain commute-mode choice after demographic characteristics are considered. Rather than assuming a linear relationship, they treated mode choice as a classification problem and tested multiple machine-learning models using 10,150 home-based commute trips in Dhaka.

#### How they approached the analysis

- They compared three machine-learning classifiers.
- Random forest provided the strongest predictive performance.
- They used the selected model to rank built-environment variables.
- They examined nonlinear threshold effects.
- They also investigated interaction effects among built-environment variables.

#### Main research contribution

The study found that built-environment characteristics contributed substantially to explaining commute-mode choice and, in that context, could be more influential than socioeconomic variables. The results also showed that infrastructure effects were not constant: certain variables became influential only after reaching particular thresholds.

#### Research gap

Earlier studies often relied on linear assumptions or examined isolated built-environment variables. The paper addressed the need to capture nonlinear and interacting effects in a dense and rapidly developing metropolitan context.

#### Limitations and future potential

The findings are specific to Dhaka and may not transfer directly to lower-density U.S. metropolitan areas. Cross-sectional data also limit causal interpretation. Future work can test whether identified thresholds hold in other cities, incorporate longitudinal data, explore additional travel purposes, and apply causal or quasi-experimental methods.

#### Relevance to this challenge

This paper demonstrates why demographic similarity alone is insufficient. It provides a model for examining whether transportation supply and urban form explain differences in travel outcomes and shows how explainable machine learning can reveal thresholds and interactions.

---

### Paper 2

**Naseralavi, S., Soltanirad, M., Ranjbar, E., Lucero, M., Gorzin, F., Hakiminejad, Y., Azimi, S., Baghersad, M., and Mazaheri, A. (2025). “Machine Learning Modeling of Household Trip Generation by State Using NHTS Data.” Urban Science, 9(9), 353. DOI: 10.3390/urbansci9090353.**

#### How the authors shaped the problem

The authors questioned whether one national trip-generation model can adequately represent travel behavior across different U.S. states. Their central argument was that the effects of variables such as household size, income, employment, and vehicle ownership may differ geographically.

#### How they approached the analysis

The study used National Household Travel Survey data in a two-stage framework:

1. It compared CatBoost, random forest, and linear regression as benchmark trip-generation models.
2. It then developed state-specific models to examine geographic variation in the importance and direction of explanatory factors.

An important finding was that more complex machine-learning models were not automatically superior. Linear regression remained competitive and performed best in many states, while also offering stronger interpretability.

#### Main research contribution

The paper showed that trip-generation relationships are spatially heterogeneous. A variable that strongly explains household trips in one state may have a weaker or different effect elsewhere. This challenges the use of a universal, one-size-fits-all behavioral model.

#### Research gap

Much trip-generation modeling emphasizes predictive performance while assuming that behavioral relationships are reasonably stable across geography. The study addressed the need for place-specific and interpretable models.

#### Limitations and future potential

The study relies on cross-sectional survey data and state-level modeling, which can conceal variation within metropolitan regions and neighborhoods. Future work identified by the authors includes longitudinal analysis, finer spatial resolution, richer built-environment and transportation-supply variables, and stronger integration of context-sensitive modeling.

#### Relevance to this challenge

This paper directly supports the project’s premise: similar demographic inputs do not guarantee similar trip outcomes because relationships vary by place. It also offers an important methodological lesson for students—always compare a complex model with a simple interpretable baseline.

---


## 8. Where Does AI and Machine Learning Fit?

Artificial Intelligence is **not** the objective of this challenge—it is the analytical tool that enables researchers to discover patterns that are difficult to identify using traditional statistical analysis alone. The transportation question remains the same: *why do similar neighborhoods behave differently?* AI provides a richer set of techniques for exploring, modeling, interpreting, and validating possible explanations.

Rather than replacing transportation knowledge, AI complements it. Domain knowledge is required to define meaningful neighborhood similarity, select appropriate variables, interpret model outputs, distinguish correlation from plausible mechanisms, and evaluate whether the discovered relationships make transportation sense.

AI and ML can contribute in several stages of the investigation:

- **Pattern discovery:** identify neighborhoods with similar demographic profiles using clustering or nearest-neighbor methods.
- **Feature engineering:** combine multiple transportation, accessibility, and land-use variables into more informative indicators.
- **Prediction:** estimate travel outcomes from demographic and contextual variables.
- **Explanation:** determine which variables contribute most to the observed differences using interpretable AI techniques.
- **Hypothesis generation:** reveal unexpected relationships that can motivate deeper transportation analysis.

### Possible AI/ML Methods (from simple to advanced)

| Complexity | Representative Methods | Possible Role in this Challenge |
|------------|------------------------|---------------------------------|
| Very Simple | Correlation analysis, PCA, k-means clustering | Explore data structure and identify similar neighborhoods. |
| Simple | Linear Regression, Logistic Regression | Establish interpretable baseline relationships. |
| Moderate | Decision Trees, Random Forests | Capture nonlinear relationships and rank important factors. |
| Moderate–Advanced | Gradient Boosting (XGBoost, LightGBM, CatBoost) | Improve predictive performance and identify complex interactions. |
| Advanced | Support Vector Machines, Gaussian Processes | Model more complex decision boundaries when appropriate. |
| Very Advanced | Deep Neural Networks | Useful only for very large, high-dimensional datasets; generally unnecessary for this challenge. |
| Explainable AI | SHAP, Permutation Importance, Partial Dependence, LIME | Interpret model behavior and explain why predictions differ across neighborhoods. |
| Spatial AI | Graph Neural Networks, Graph-based Learning | Represent transportation networks and neighborhood connectivity directly. Typically beyond the scope of this project. |
| Causal AI | Causal Graphs, Double Machine Learning, Causal Forests | Estimate intervention effects rather than simple associations. Usually requires stronger assumptions and richer data. |

For this challenge, the most appropriate workflow is to begin with an interpretable baseline (for example, linear regression), compare it with a tree-based model such as a random forest or gradient boosting model, and then use explainable AI techniques to understand *why* the models reached their conclusions. The emphasis should remain on generating defensible transportation insights rather than maximizing predictive accuracy.


## 9. Recommended Analytical Workflow

### Phase 1: Define the comparison

1. Select four to seven demographic variables.
2. Standardize the variables.
3. Group similar tracts using clustering or calculate nearest demographic neighbors.
4. Select one travel outcome.
5. Identify pairs with small demographic distance and large travel-outcome difference.

### Phase 2: Investigate candidate explanations

For each selected pair:

1. map both neighborhoods;
2. compare transit access;
3. compare street connectivity;
4. compare destination and employment accessibility;
5. compare roadway and congestion conditions;
6. compare trip purposes and trip distances;
7. examine crash or safety conditions when relevant; and
8. document important missing variables.

### Phase 3: Use AI or machine learning

Train an interpretable model to predict the selected travel outcome using:

- demographic variables alone; and then
- demographic plus transportation, accessibility, and land-use variables.

Compare the two models. If the second model performs meaningfully better, this provides evidence that the added contextual factors explain travel differences that demographics alone could not explain.

Representative models include:

- linear or logistic regression as the baseline;
- random forest or gradient boosting as the nonlinear model; and
- permutation importance or SHAP for interpretation.

### Phase 4: Validate the explanation

The analysis should not accept the first high-importance feature as the answer. They should verify whether:

- it is consistent across several neighborhood pairs;
- it has a plausible transportation mechanism;
- it is not simply duplicating another variable;
- the result persists when an unusual tract is removed; and
- the conclusion remains reasonable on a map.

### Phase 5: Communicate the result

The final explanation should contain:

- the definition of demographic similarity;
- the selected travel outcome;
- a map of selected neighborhoods;
- evidence that the neighborhoods are demographically similar;
- evidence that their travel patterns differ;
- the most important explanatory factors;
- model-performance comparison;
- limitations and missing data; and
- one or two realistic planning implications.

---

## 10. How the Answer Can Improve Transportation Systems

The answer can help transportation agencies distinguish between travel behavior driven primarily by household circumstances and behavior driven by transportation or land-use constraints.

Possible applications include:

- identifying neighborhoods where transit availability does not match potential demand;
- targeting pedestrian or bicycle improvements;
- improving connections to employment centers;
- locating first-mile and last-mile gaps;
- prioritizing transit-service improvements;
- recognizing where automobile dependence results from limited alternatives rather than simple preference;
- improving trip-generation and mode-choice models;
- designing geographically specific transportation-demand-management strategies; and
- evaluating whether transportation investments are distributed equitably.

The most useful result is not a statement that one variable “causes” a travel pattern. It is a ranked and evidence-based explanation of which factors appear to separate otherwise comparable neighborhoods and what interventions could reasonably be tested.

---

## 11. Expected Final Program Outcome

By the end of the program, the team should present a clear comparison of several demographically similar Dallas County neighborhoods that exhibit substantially different travel behavior.

A successful project should include:

1. a reproducible definition of demographic similarity;
2. a clearly defined travel-pattern outcome;
3. at least three meaningful neighborhood comparisons;
4. integration of at least four datasets;
5. maps and visual evidence;
6. one baseline statistical model;
7. one interpretable machine-learning model;
8. a ranked set of explanatory factors;
9. discussion of uncertainty, missing variables, and the difference between association and causation; and
10. practical transportation-planning implications.

### Example of an acceptable final conclusion

> The team identified four pairs of Census tracts with similar income, age, education, employment, and vehicle availability but substantially different automobile commute shares. Adding transit accessibility, job proximity, intersection density, and destination density improved the model compared with demographics alone. Across most pairs, the lower-driving tract had better job accessibility and denser transit and street networks. Transit-stop density by itself was not sufficient; it was most useful when combined with nearby destinations and shorter travel distances. The evidence suggests that differences in transportation and land-use context help explain the observed behavior, although parking conditions, transit reliability, and household preferences could not be measured. The team recommends prioritizing accessibility and network connectivity rather than adding isolated transit stops.

This level of conclusion is appropriate because it is specific, supported by evidence, cautious about causality, and connected to a potential transportation decision.

---

## 12. Minimum Scope for the Academy

Because the working period is limited, students are not expected to build a comprehensive behavioral travel-demand model.

The minimum viable project is:

- Census tracts as neighborhoods;
- five demographic similarity variables;
- one primary travel outcome;
- three to five contrasting neighborhood pairs;
- four integrated datasets;
- one baseline model;
- one tree-based model;
- feature-importance analysis;
- two maps;
- a limitations section; and
- one actionable planning recommendation.

The project should prioritize defensible reasoning and clear evidence over model complexity.
