# Research Challenge 3
# What Factors Contribute to Differences in Crash Occurrence Across Dallas County?

---

# 1. Challenge Overview

Roadway safety is one of the fundamental objectives of transportation engineering. Every day, millions of trips are completed safely, yet a relatively small number result in crashes that can lead to injuries, fatalities, traffic delays, property damage, and significant economic costs. Understanding why crashes occur—and why some locations experience substantially more crashes than others—remains one of the most important research problems in modern transportation systems.

At first glance, crash occurrence may appear to be explained by obvious roadway characteristics such as traffic volume, speed limit, or roadway geometry. However, transportation agencies have long observed that locations with very similar physical and operational characteristics often exhibit remarkably different safety performance. Two roadway segments may have the same number of lanes, similar traffic volumes, and identical speed limits, yet one consistently experiences more crashes than the other. Likewise, two intersections with comparable traffic demand and geometric design may produce very different crash histories.

These differences suggest that roadway safety is influenced by much more than roadway geometry alone. Crash occurrence emerges from the interaction of roadway design, traffic operations, surrounding land use, environmental conditions, infrastructure, travel demand, and human behavior. Some of these factors can be measured directly, while others remain hidden or difficult to observe using publicly available data.

The objective of this challenge is to investigate why these differences exist by integrating multiple transportation, infrastructure, environmental, and demographic datasets describing Dallas County. Rather than focusing solely on predicting crash locations, the emphasis is on developing an evidence-based explanation for the factors that are most strongly associated with crash occurrence.

Artificial Intelligence and Machine Learning play an important supporting role throughout this investigation. They provide powerful analytical tools for discovering complex relationships, identifying influential variables, and revealing patterns that may not be obvious through traditional statistical analysis. However, the primary objective remains transportation understanding rather than model development.

A useful way to frame this research challenge is:

> **After controlling for roadway geometry and traffic exposure, which transportation, operational, environmental, and community characteristics best explain why some roadway locations experience substantially more crashes than other physically similar locations across Dallas County?**

Answering this question can help transportation agencies better understand roadway safety, prioritize engineering improvements, and make more informed decisions when investing in future transportation infrastructure.

# 2. Why This Challenge Matters in Transportation

Roadway safety is one of the primary measures used to evaluate the performance of a transportation system. While congestion affects travel time and reliability, crashes have far more serious consequences, including fatalities, injuries, property damage, emergency response costs, environmental impacts, and significant economic losses. For transportation agencies, improving safety is therefore not only an engineering objective but also a public health and societal responsibility.

Every year, agencies invest substantial resources in roadway improvements, traffic control devices, intersection redesign, speed management, and safety programs. Because budgets are limited, these investments must be prioritized carefully. Understanding **why** certain locations experience higher crash occurrence is therefore just as important as knowing **where** crashes happen.

Historically, safety analyses have focused on identifying crash hotspots by ranking locations according to historical crash frequency. Although this approach is useful for identifying locations that require further investigation, it provides only a partial understanding of roadway safety. High crash counts may simply reflect high traffic volumes, while locations with relatively few crashes may actually present greater risk when traffic exposure is considered.

Modern transportation engineering increasingly emphasizes understanding the mechanisms that contribute to crash occurrence rather than relying solely on historical crash records. Instead of asking where crashes have already happened, agencies seek to understand which roadway characteristics, operational conditions, and surrounding environments increase the likelihood of future crashes. This shift from reactive to proactive safety management allows transportation professionals to identify potential risks before serious safety problems develop.

This challenge supports that modern perspective by encouraging a systems-level investigation of roadway safety. Rather than assuming that roadway geometry alone determines crash occurrence, it considers how infrastructure, traffic operations, land use, demographics, accessibility, and environmental conditions interact to influence roadway performance.

The knowledge gained from this type of analysis has numerous practical applications. Transportation agencies can use the results to prioritize roadway improvements, evaluate design alternatives, improve access management, optimize traffic operations, support Vision Zero initiatives, and guide future infrastructure investments. More broadly, understanding the factors associated with crash occurrence contributes to safer, more efficient, and more resilient transportation systems.

Perhaps most importantly, this challenge illustrates how transportation engineering is evolving into a data-driven discipline. Today, roadway safety decisions increasingly rely on integrating diverse datasets and applying advanced analytical techniques rather than evaluating crash records in isolation. Artificial Intelligence expands the ability to analyze these complex datasets, but meaningful transportation improvements still depend on sound engineering interpretation and evidence-based decision making.

# 3. Why Finding the Answer Is Difficult

Unlike many engineering problems, roadway safety cannot be explained by a single variable or a simple cause-and-effect relationship. Traffic crashes result from the interaction of roadway design, traffic conditions, environmental factors, surrounding land use, and human behavior. These factors influence one another continuously, making crash occurrence one of the most complex problems in transportation engineering.

One of the first challenges is that crashes are relatively **rare events**. Every day, millions of vehicles travel safely through the transportation network, while only a very small percentage of trips result in crashes. This means that crash datasets contain far more examples of normal roadway operation than crash events, making statistical analysis and machine-learning modeling more difficult.

Another challenge is distinguishing **crash frequency** from **crash risk**. A roadway carrying 100,000 vehicles per day will naturally experience more crashes than a local residential street simply because many more vehicle interactions occur. High crash counts do not necessarily indicate poor roadway design. For this reason, traffic exposure—often represented by measures such as Average Annual Daily Traffic (AADT)—must be considered before comparing roadway safety across different locations.

Defining what makes two roadway locations "similar" is also more complicated than it initially appears. Two roadway segments may share the same speed limit, number of lanes, and functional classification while differing in access density, nearby commercial activity, pedestrian demand, signal coordination, or intersection spacing. These differences may substantially influence crash occurrence even though the roadways appear similar based on a few basic characteristics.

Roadway safety is further complicated by the influence of **human behavior**, which is one of the most important but least measurable components of the transportation system. Factors such as distraction, fatigue, aggressive driving, speeding, driver experience, and compliance with traffic laws are rarely available in public datasets. As a result, even the best analytical models cannot fully explain every crash.

Crash occurrence also exhibits strong **spatial and temporal variability**. Neighboring roadway segments influence one another through congestion, rerouting, and network connectivity, while weather, time of day, day of week, and seasonal travel patterns continuously change roadway operating conditions. A location that operates safely during one period may experience elevated crash risk under different environmental or traffic conditions.

Another important consideration is that **correlation does not imply causation**. Machine-learning models may identify variables that are strongly associated with crash occurrence, but these variables are not necessarily the direct cause of crashes. For example, commercial land use may appear highly influential because it is associated with increased turning movements, pedestrian activity, and driveway density rather than because commercial development itself creates unsafe conditions. Transportation engineering knowledge is therefore essential for interpreting analytical results correctly.

Finally, roadway safety should be viewed as a **systems problem** rather than a collection of independent roadway locations. Every roadway segment is part of a larger transportation network in which infrastructure, traffic operations, land use, mobility patterns, and human behavior interact continuously. Understanding these interactions is far more valuable than simply identifying locations with high crash frequencies.

For these reasons, the objective of this challenge is not to discover a single variable that explains crash occurrence. Instead, the goal is to identify combinations of factors that consistently help explain why apparently similar roadway environments exhibit different safety performance and to interpret those findings within the broader context of transportation engineering.

# 4. Measurable Structural Factors and Hidden (Latent) Factors

A useful way to study roadway safety is to separate the factors influencing crash occurrence into two broad categories: **measurable structural factors** and **hidden (latent) factors**.

Measurable factors are variables that can be obtained directly from transportation, GIS, demographic, environmental, or operational datasets. These variables form the foundation of quantitative analysis because they can be integrated into statistical and machine-learning models.

Latent factors represent important influences that cannot be observed directly or are unavailable within public datasets. Although these variables may strongly affect roadway safety, they must often be acknowledged qualitatively rather than modeled explicitly.

Recognizing the difference between these two categories is important because it helps establish realistic expectations for the analysis. Machine-learning models can only discover relationships among the variables they are given. They cannot account for influential factors that are missing from the data.

---

## Measurable Structural Factors

The first category consists of observable characteristics describing the roadway and its surrounding environment.

### Roadway Characteristics

Roadway geometry influences how vehicles interact within the transportation network. Representative variables include:

- roadway functional classification;
- posted speed limit;
- number of lanes;
- median type;
- intersection type;
- roadway connectivity;
- access density; and
- roadway curvature.

These characteristics define the physical environment in which traffic operates and are often used to establish roadway similarity.

---

### Traffic Characteristics

Traffic conditions describe how the roadway is used.

Representative variables include:

- Average Annual Daily Traffic (AADT);
- hourly traffic volume;
- operating speed;
- speed variability;
- congestion level;
- heavy-vehicle percentage; and
- travel time reliability.

These variables help distinguish differences caused by traffic demand from those associated with roadway design.

---

### Transportation Infrastructure

Infrastructure influences the number and complexity of interactions among road users.

Examples include:

- traffic signals;
- pedestrian crossings;
- sidewalks;
- bicycle facilities;
- roadway lighting;
- transit stops;
- traffic control devices; and
- access management.

Well-designed infrastructure can reduce conflict opportunities even under relatively high traffic demand.

---

### Land Use and Accessibility

Roadways serve the communities surrounding them, making land-use characteristics an important part of roadway safety analysis.

Examples include:

- residential density;
- commercial development;
- employment density;
- schools;
- hospitals;
- parks;
- shopping centers;
- accessibility to employment; and
- accessibility to transit.

These variables influence travel demand, turning movements, pedestrian activity, and overall roadway complexity.

---

### Demographic and Environmental Characteristics

Additional variables describing surrounding communities and environmental conditions include:

- population density;
- household income;
- educational attainment;
- vehicle ownership;
- commuting characteristics;
- rainfall;
- visibility;
- temperature;
- time of day; and
- seasonal conditions.

These variables do not directly determine crash occurrence but often influence travel behavior and roadway operating conditions.

---

## Hidden (Latent) Factors

Even after integrating multiple transportation datasets, several important contributors to roadway safety remain difficult or impossible to measure directly.

Examples include:

- driver distraction;
- fatigue;
- aggressive driving;
- reaction time;
- familiarity with the roadway;
- temporary traffic conditions;
- adaptive signal timing;
- queue formation;
- special events;
- vehicle maintenance;
- advanced driver-assistance systems;
- emergency response; and
- individual risk perception.

Many of these factors vary from one trip to another and are not recorded systematically in publicly available transportation datasets.

Consequently, analytical models cannot fully explain every crash or identify every contributing factor.

---

## Why This Distinction Matters

Separating measurable and latent factors provides a more realistic understanding of what transportation data can and cannot explain.

For example, a machine-learning model may identify commercial land use as one of the most influential variables associated with crash occurrence. This does not necessarily mean that commercial development causes crashes. Instead, commercial areas often coincide with higher traffic volumes, more driveways, increased pedestrian activity, and greater turning movements. In this case, commercial land use may be acting as a proxy for several interacting roadway characteristics.

Similarly, roadway geometry may appear less influential than expected because driver behavior or temporary operational conditions—variables that are not directly observable—play an important role.

For this reason, the results of this challenge should be interpreted as identifying **relationships among observable transportation variables**, not as providing a complete explanation of roadway safety.

The strongest transportation studies recognize these limitations explicitly and combine analytical evidence with engineering judgment when developing conclusions and recommendations.

## Helper Functions That Support Measurable Factors

Several roadway-safety factors can be created with helper functions instead of being coded from scratch:

- `summarize_street_connectivity` for roadway connectivity, intersection density, road density, dead ends, links per node, and average segment length;
- `summarize_points_within_distance` for traffic signals, transit stops, schools, hospitals, crashes, employers, destinations, and other point features near a roadway or area;
- `summarize_lines_within_distance` for nearby bikeways, trails, freight corridors, transit routes, major roads, and roadway exposure;
- `summarize_polygons_within_distance` for nearby land use, parks, school zones, development areas, and service areas;
- `add_nearest_distance` for proximity to transit, employment centers, major roads, hospitals, parks, and other activity centers;
- `calculate_facility_coverage` for the share of an area covered by buffered facilities such as transit stops, trails, bikeways, or parks; and
- `calculate_land_use_mix` for land-use diversity after land-use area has been summarized by category.

# 5. How to Think About the Problem

A common mistake in roadway safety analysis is to begin by applying statistical or machine-learning models to crash data without first defining the transportation question. While predictive models may identify statistical relationships, they do not automatically explain why those relationships exist. Meaningful transportation research begins by developing a logical framework for comparing roadway environments and then evaluating whether the available evidence supports the proposed explanations.

This challenge is based on the idea of **controlled comparison**. Rather than comparing completely different roadway environments, the analysis should first identify roadway locations that are broadly similar in their physical and operational characteristics. Once these comparable locations have been established, additional datasets can be examined to determine which factors are consistently associated with differences in crash occurrence.

### Step 1: Define the Unit of Analysis

The first decision is selecting the spatial unit of analysis. Depending on the available data, the investigation may focus on roadway segments, intersections, traffic analysis zones, or other geographic units. Whatever unit is selected should remain consistent throughout the project so that all datasets can be integrated and compared reliably.

### Step 2: Establish Roadway Similarity

Before examining crash occurrence, define what makes two roadway locations similar.

Typical similarity variables may include:

- roadway functional classification;
- posted speed limit;
- number of lanes;
- roadway type;
- traffic exposure (AADT);
- intersection control type; and
- urban or suburban context.

These variables establish a baseline level of comparability. Additional explanatory variables should only be introduced after similar roadway environments have been identified.

### Step 3: Select the Safety Outcome

Roadway safety can be represented in several ways, including:

- total crash frequency;
- crash rate;
- injury crashes;
- severe crashes;
- pedestrian crashes; or
- intersection-related crashes.

Selecting one primary outcome simplifies interpretation and allows the investigation to remain focused. Additional crash types can always be explored later if time permits.

### Step 4: Integrate Complementary Datasets

Crash data alone rarely explain why crashes occur. Additional datasets should be integrated to describe the roadway environment more completely.

Useful information may include:

- roadway geometry;
- traffic characteristics;
- transportation infrastructure;
- demographic data;
- land use;
- environmental conditions;
- accessibility measures; and
- mobility patterns.

The objective is to build a comprehensive representation of each roadway location rather than relying on a single source of information.

### Step 5: Explore Before Modeling

Exploratory analysis is an essential part of transportation research.

Before building predictive models, the data should be examined through:

- descriptive statistics;
- maps;
- scatter plots;
- correlation analysis;
- summary tables; and
- spatial visualizations.

These techniques often reveal trends, anomalies, and relationships that help guide later modeling decisions.

### Step 6: Develop Interpretable Models

Once the data have been explored, analytical models can be developed to investigate which variables are most strongly associated with crash occurrence.

A useful strategy is to begin with an interpretable statistical model, such as Poisson Regression or Negative Binomial Regression, and then compare its results with one or more machine-learning models, such as Random Forest or Gradient Boosting.

Using multiple approaches allows the analysis to balance interpretability with the ability to capture nonlinear relationships.

### Step 7: Interpret the Results

The final objective is not to produce a ranked list of important variables but to understand what those variables represent from a transportation engineering perspective.

Questions worth considering include:

- Are the identified relationships consistent across multiple roadway comparisons?

- Do the results agree with established transportation engineering principles?

- Could an important latent factor explain part of the observed relationship?

- Are the findings practically useful for transportation agencies?

Answering these questions transforms statistical output into transportation knowledge.

### Think Like a Transportation Researcher

Throughout the project, it is helpful to think of the analysis as a process of evaluating hypotheses rather than searching for a single correct answer.

Every result should be viewed as one piece of evidence within a broader transportation system. Multiple datasets, multiple analytical methods, and engineering reasoning should work together to build confidence in the final conclusions.

The strongest investigations rarely claim that one variable causes crashes. Instead, they identify combinations of roadway, operational, environmental, and community characteristics that are consistently associated with crash occurrence and then explain those relationships using established transportation engineering principles.

Ultimately, success in this challenge depends less on selecting a particular algorithm and more on asking thoughtful questions, integrating diverse sources of evidence, and developing conclusions that are both analytically sound and practically meaningful.

# 6. Data That Can Help Answer the Challenge

One of the defining characteristics of transportation research is that important questions rarely can be answered using a single dataset. Crash records identify **where** and **when** crashes occurred, but they rarely explain **why** they occurred. Understanding roadway safety requires integrating multiple datasets that describe different aspects of the transportation system and the surrounding environment.

The objective of this challenge is therefore not simply to analyze crash data, but to combine complementary datasets into a unified view of each roadway location. Each dataset contributes a different perspective, and together they provide a more complete understanding of the conditions associated with crash occurrence.

---

## Available Data

### Crash Data

Crash records provide the primary outcome for this challenge. They describe the location, time, severity, and characteristics of reported crashes and establish the basis for comparing roadway safety across Dallas County.

### Roadway Inventory

Roadway inventory datasets describe the physical characteristics of the transportation network, including roadway classification, speed limits, lane configuration, intersection types, and other geometric features. These variables are essential for defining roadway similarity.

### Traffic Characteristics

Traffic datasets provide measures of roadway use, including Average Annual Daily Traffic (AADT), hourly traffic volume, operating speeds, and congestion indicators. These variables help account for traffic exposure and distinguish between busy roadways and genuinely high-risk locations.

### Transportation Infrastructure

Infrastructure datasets describe facilities that influence traffic operations and roadway interactions, including traffic signals, pedestrian crossings, sidewalks, bicycle facilities, transit stops, and roadway lighting. These variables provide important context for understanding how roadway design influences safety.

### GIS and Land Use

Geographic datasets describe the environment surrounding each roadway. Commercial development, residential neighborhoods, schools, hospitals, parks, employment centers, and roadway connectivity all influence travel demand and the complexity of vehicle, pedestrian, and bicycle interactions.

### Demographic Data

Census and American Community Survey (ACS) datasets provide information about the communities served by the transportation network, including population density, household income, vehicle ownership, commuting behavior, educational attainment, and age distribution. These variables help explain differences in travel demand and roadway use.

### Mobility Data

Origin–Destination (OD) datasets, such as Replica, provide information about travel patterns, trip purposes, and movement throughout the county. These data offer valuable insight into how roadway demand varies across different locations and times.

### Environmental Data

Weather observations, daylight conditions, and seasonal information provide additional context for understanding roadway operating conditions. Rainfall, visibility, and temperature can all influence driver behavior and crash probability.

---

## Data That Are Difficult to Obtain

Although the available datasets describe many important aspects of the transportation system, several influential variables remain difficult to measure.

Examples include:

- driver distraction and fatigue;
- aggressive driving behavior;
- detailed signal timing and adaptive signal control;
- vehicle trajectories and near-miss events;
- pedestrian and bicycle volumes;
- temporary roadway conditions;
- special events and unusual traffic patterns;
- advanced driver-assistance technologies.

These variables often play an important role in roadway safety but are rarely available at a county-wide scale.

---

## Why Missing Data Matter

The absence of these datasets does not prevent meaningful analysis, but it does influence how the results should be interpreted.

Machine-learning models identify relationships among the variables that are available, not necessarily among all variables that influence crash occurrence. Consequently, an important variable in the model may sometimes act as a proxy for another factor that could not be measured directly.

For example, commercial land use may represent increased turning movements, pedestrian activity, or driveway density rather than being a direct cause of crashes. Similarly, traffic volume may represent exposure rather than roadway quality.

Recognizing these limitations is an important part of responsible transportation research. The objective is not to identify every factor affecting roadway safety, but to develop the most complete explanation possible using the available evidence while acknowledging the uncertainty introduced by missing information.

# 7. Where Does Artificial Intelligence and Machine Learning Fit?

Artificial Intelligence is **not** the objective of this research challenge. The objective is to understand why roadway locations with similar physical and operational characteristics experience different crash occurrence. AI and Machine Learning provide analytical tools that help investigate this question by discovering patterns, modeling complex relationships, and generating evidence that supports transportation engineering decisions.

Roadway safety has traditionally been studied using statistical models such as **Poisson Regression** and **Negative Binomial Regression**, which remain the standard methods for analyzing crash count data. These models are highly interpretable and continue to play an important role in transportation safety research. However, modern transportation systems generate large volumes of heterogeneous data describing infrastructure, traffic operations, land use, demographics, mobility, and environmental conditions. The relationships among these variables are often nonlinear and difficult to capture using traditional methods alone.

Machine learning complements—not replaces—these statistical approaches by providing additional analytical capabilities.

---

## How AI Can Support This Challenge

Artificial Intelligence can contribute throughout different stages of the investigation.

### Pattern Discovery

Unsupervised learning techniques can identify roadway locations with similar characteristics before crash occurrence is analyzed.

Representative methods include:

- K-Means Clustering;
- Hierarchical Clustering;
- DBSCAN; and
- Principal Component Analysis (PCA).

These techniques help organize large datasets and reveal natural groupings within the transportation network.

---

### Feature Engineering

Machine learning can also assist in creating new explanatory variables by combining multiple datasets.

Examples include:

- roadway complexity indices;
- accessibility measures;
- intersection density;
- land-use diversity;
- multimodal accessibility; and
- crash exposure indicators.

These derived features often describe roadway environments more effectively than individual raw variables.

---

### Predictive Modeling

Once the datasets have been integrated, machine-learning models can estimate crash occurrence and identify variables associated with elevated roadway risk.

Representative models include:

- Decision Trees;
- Random Forests;
- Gradient Boosting;
- XGBoost; and
- LightGBM.

The purpose of these models is not only to make predictions but also to identify relationships that deserve further engineering investigation.

---

### Explainable AI

Interpretability is particularly important in transportation engineering because agencies must understand **why** a model reaches its conclusions before using those results to support infrastructure investments.

Explainable AI techniques include:

- SHAP values;
- Permutation Importance;
- Partial Dependence Plots (PDP); and
- LIME.

These methods help answer questions such as:

- Which variables contribute most to crash occurrence?
- How do different variables interact?
- Are there threshold effects or nonlinear relationships?
- Do roadway, operational, and demographic factors contribute equally?

Explainability transforms machine-learning models from prediction tools into decision-support tools.

---

## Choosing the Right Model

More complex models do not necessarily produce better transportation insight. In many cases, an interpretable model that clearly explains the relationships among variables is more valuable than a highly accurate black-box model.

The following progression illustrates how different analytical methods may contribute to this challenge.

| Complexity | Representative Methods | Primary Purpose |
|------------|------------------------|-----------------|
| **Exploratory** | Correlation Analysis, PCA, Clustering | Understand the data and identify similar roadway environments. |
| **Baseline Statistical Models** | Poisson Regression, Negative Binomial Regression | Develop interpretable models for crash occurrence and establish a benchmark for comparison. |
| **Machine Learning** | Decision Trees, Random Forests, Gradient Boosting | Capture nonlinear relationships and interactions among explanatory variables. |
| **Explainable AI** | SHAP, Permutation Importance, PDP, LIME | Interpret model predictions and quantify the influence of individual variables. |
| **Advanced Research Methods** | Graph Neural Networks (GNN), Graph Attention Networks (GAT), Causal AI | Model spatial interactions and investigate more advanced transportation research questions beyond the scope of this project. |

---

## AI and Transportation Engineering Work Together

Artificial Intelligence identifies patterns within data, but it cannot determine whether those patterns represent meaningful transportation mechanisms. Transportation engineering provides the theoretical foundation needed to interpret analytical results, evaluate their plausibility, and translate them into practical recommendations.

For example, if a machine-learning model identifies access density as an influential variable, transportation engineering knowledge is required to explain **why** increased access points create additional conflict opportunities and how roadway design could be improved.

Similarly, if commercial land use appears highly associated with crash occurrence, engineering reasoning is needed to determine whether the relationship reflects turning movements, pedestrian activity, traffic demand, or another underlying factor.

For this reason, the most successful investigations combine AI with transportation expertise. Machine learning discovers relationships, while transportation engineering determines whether those relationships are meaningful, actionable, and consistent with established roadway safety principles.

The goal is not to build the most sophisticated AI model. The goal is to use AI responsibly to develop a deeper understanding of roadway safety and support better transportation decisions.

# 8. Recommended Analytical Workflow

The following workflow provides a structured approach for investigating the research challenge. Although different analytical techniques may be used, the overall process should remain focused on understanding the transportation system rather than simply developing predictive models.

---

## Phase 1 – Define the Research Problem

Begin by clearly defining the transportation question.

Identify:

- the unit of analysis (roadway segment, intersection, or another spatial unit);
- the crash outcome to be investigated;
- the roadway characteristics used to establish similarity; and
- the geographic scope of the analysis.

A well-defined research question provides direction for every subsequent stage of the project.

---

## Phase 2 – Prepare and Integrate the Data

Collect and combine datasets describing different aspects of the transportation system.

Typical sources include:

- crash records;
- roadway inventory;
- traffic characteristics;
- transportation infrastructure;
- land use;
- demographic information;
- mobility data; and
- environmental conditions.

Before analysis, the datasets should be cleaned, standardized, and spatially integrated so that each roadway location is described consistently across all data sources.

---

## Phase 3 – Explore the Data

Conduct exploratory data analysis to understand the characteristics of the integrated dataset.

Useful techniques include:

- descriptive statistics;
- maps;
- scatter plots;
- histograms;
- correlation matrices;
- roadway comparison tables; and
- spatial visualizations.

This phase helps identify unusual observations, missing data, and preliminary relationships that may guide the modeling process.

---

## Phase 4 – Develop and Compare Models

Begin with an interpretable statistical model, such as Poisson Regression or Negative Binomial Regression, to establish a baseline understanding of crash occurrence.

Then develop one or more machine-learning models, such as Random Forest or Gradient Boosting, to investigate nonlinear relationships and interactions among variables.

Rather than selecting a single "best" model, compare how different approaches explain the observed crash patterns.

---

## Phase 5 – Interpret the Results

Use explainable AI techniques and transportation engineering principles to interpret the analytical results.

Important questions include:

- Which variables consistently appear influential?

- Do the results agree with established transportation engineering knowledge?

- Are the identified relationships physically reasonable?

- Could hidden variables explain part of the observed behavior?

Interpretation is often the most valuable stage of the entire project because it transforms analytical output into engineering knowledge.

---

## Phase 6 – Develop Practical Recommendations

The final step is translating the findings into recommendations that transportation agencies could realistically use.

Examples include:

- prioritizing roadway safety improvements;
- improving access management;
- modifying roadway design;
- optimizing traffic operations;
- identifying locations requiring further engineering investigation; and
- recommending additional data collection.

A successful project should conclude by explaining not only **what** was discovered, but also **how those discoveries could help improve roadway safety across Dallas County.**

# 9. Representative Research Papers

Transportation safety has been studied for decades using statistical modeling, roadway engineering, and more recently, Artificial Intelligence. Early research primarily focused on identifying relationships between roadway characteristics and crash frequency using regression-based approaches. More recent studies increasingly integrate machine learning, explainable AI, and network-based modeling to better understand the complex interactions that influence crash occurrence.

The following two representative papers illustrate how modern transportation researchers investigate roadway safety and how Artificial Intelligence can be combined with transportation engineering to produce meaningful, interpretable results.

---

## Paper 1

### Li, J., Wang, X., Yang, X., Zhang, Q., & Pan, H. (2024)

**Analyzing Freeway Safety Influencing Factors Using the CatBoost Model and Interpretable Machine-Learning Framework (SHAP)**

*Transportation Research Record*

### Research Problem

The authors recognized that traditional crash prediction models often struggle to capture the complex nonlinear relationships among roadway geometry, traffic conditions, and crash occurrence. At the same time, many advanced machine-learning models improve predictive performance but provide little explanation for why their predictions are made.

The study therefore investigated whether an interpretable machine-learning framework could improve both prediction and understanding of roadway safety.

### Methodology

The researchers compared traditional statistical approaches with modern tree-based machine-learning models, including CatBoost. They then used **SHAP (SHapley Additive Explanations)** to interpret the resulting models and quantify the contribution of individual variables to crash occurrence.

### Key Findings

The study showed that explainable machine-learning models were able to identify complex nonlinear relationships while maintaining a level of interpretability suitable for transportation engineering applications. Variables such as traffic volume, roadway geometry, and roadway design features contributed differently under different operating conditions, illustrating that roadway safety cannot always be explained through simple linear relationships.

### Research Gap

Although the study demonstrated the value of explainable AI, it focused primarily on freeway characteristics and roadway design variables. Broader contextual factors such as land use, demographics, accessibility, and multimodal transportation were not fully incorporated.

### Future Research

The authors recommended integrating richer transportation datasets, improving model interpretability, and expanding analyses to more diverse roadway environments.

### Relevance to This Challenge

This paper reinforces one of the central ideas of this project: Artificial Intelligence should not simply predict crashes—it should help explain **why** crashes occur. The emphasis on explainability aligns closely with the objectives of this research challenge.

---

## Paper 2

### Gao, X., Jiang, X., Haworth, J., Zhuang, D., Wang, S., Chen, H., & Law, S. (2024)

**Uncertainty-aware Probabilistic Graph Neural Networks for Road-Level Traffic Crash Prediction**

*Accident Analysis & Prevention*

### Research Problem

Most crash prediction models treat roadway locations as independent observations. However, transportation networks are highly interconnected, and conditions on one roadway frequently influence neighboring roadways. The authors investigated whether Graph Neural Networks (GNNs) could better represent these spatial relationships while also accounting for uncertainty in crash prediction.

### Methodology

Roadway segments were represented as nodes within a transportation network, allowing the model to learn both roadway characteristics and spatial relationships simultaneously. An uncertainty-aware framework was incorporated to estimate the confidence associated with each prediction.

### Key Findings

The study demonstrated that explicitly modeling roadway connectivity improved crash prediction and better represented the spatial nature of roadway safety. It also highlighted the importance of quantifying uncertainty when analyzing rare events such as crashes.

### Research Gap

Although Graph Neural Networks improved predictive performance, they remained considerably less interpretable than traditional statistical models. Understanding **why** the model produced a particular prediction remained an important challenge.

### Future Research

The authors identified several promising research directions, including explainable graph-based models, integration with connected-vehicle data, Digital Twins, and real-time roadway safety monitoring.

### Relevance to This Challenge

This paper emphasizes that roadway safety should be viewed as a **network problem** rather than a collection of isolated roadway segments. While implementing Graph Neural Networks is beyond the scope of this project, the systems perspective introduced in this work provides valuable insight when interpreting roadway safety across Dallas County.

---

## Lessons from the Literature

Although these studies use different analytical techniques, they reach several common conclusions.

First, roadway safety is influenced by multiple interacting factors rather than any single roadway characteristic. Second, integrating diverse transportation datasets improves understanding of crash occurrence. Third, Artificial Intelligence provides valuable analytical capabilities, but transportation engineering expertise remains essential for interpreting results and developing practical recommendations.

Together, these studies support the philosophy of this challenge: combining transportation engineering, data integration, and explainable Artificial Intelligence to develop evidence-based explanations for differences in crash occurrence rather than focusing solely on predictive accuracy.

# 10. How the Answer Can Improve Transportation Systems

The ultimate purpose of this research challenge is not simply to explain crash occurrence, but to generate knowledge that can support better transportation decisions. Understanding why similar roadway locations experience different safety outcomes allows transportation agencies to move beyond reactive crash analysis and toward proactive safety management.

If the factors associated with elevated crash occurrence can be identified reliably, agencies can prioritize roadway improvements before crashes become recurring problems. Instead of relying solely on historical crash records, transportation professionals can evaluate roadway environments based on the characteristics that are consistently associated with increased crash risk.

The findings from this challenge may support a variety of engineering and planning activities, including:

- prioritizing roadway safety investments;
- improving roadway and intersection design;
- optimizing traffic operations;
- enhancing pedestrian and bicycle safety;
- improving access management;
- supporting Vision Zero initiatives;
- guiding future data collection efforts; and
- informing long-term transportation planning.

Beyond individual projects, this challenge also demonstrates the value of integrating multiple transportation datasets into a unified analytical framework. Combining roadway characteristics, traffic operations, demographics, land use, mobility, and environmental information provides a more complete understanding of roadway safety than analyzing crash records alone.

Finally, the project illustrates how Artificial Intelligence can support transportation engineering without replacing it. Machine learning helps discover patterns within large datasets, while engineering knowledge provides the context needed to interpret those patterns and translate them into practical recommendations.

A successful investigation should therefore produce more than a predictive model. It should generate evidence-based insights that help transportation agencies understand roadway safety, allocate resources more effectively, and ultimately create safer transportation systems for the communities they serve.

# 11. Expected Final Program Outcome

The purpose of this research challenge is not to produce a production-ready crash prediction system or to identify a single definitive cause of roadway crashes. Instead, the goal is to complete a structured transportation research investigation that combines multiple datasets, applies appropriate analytical methods, and develops an evidence-based explanation for differences in crash occurrence across similar roadway environments.

By the end of the project, the investigation should demonstrate how transportation engineering, data science, and Artificial Intelligence can be integrated to address a real-world transportation problem.

A successful project should include:

- a clearly defined transportation research question;
- a reproducible methodology for identifying similar roadway locations;
- an integrated dataset representing multiple aspects of the transportation system;
- exploratory data analysis supported by appropriate visualizations;
- at least one interpretable statistical model;
- at least one machine-learning model;
- explainable AI results that help interpret the model;
- an engineering discussion of the findings;
- a clear description of study limitations; and
- practical recommendations supported by evidence.

The final conclusions should focus on explaining **why** differences in crash occurrence were observed rather than simply reporting model accuracy or feature rankings.

An example of an appropriate conclusion might be:

> Roadway segments with similar traffic exposure and geometric characteristics exhibited different crash occurrence after controlling for roadway type and traffic volume. The integrated analysis consistently identified access density, commercial development, intersection spacing, and operating conditions as influential variables. These findings suggest that roadway complexity, rather than roadway geometry alone, plays an important role in explaining crash occurrence across Dallas County. Although several important behavioral and operational variables were unavailable, the results provide evidence that can support future engineering investigations and targeted roadway safety improvements.

Ultimately, the strongest projects will demonstrate thoughtful transportation reasoning, effective use of data, and well-supported conclusions rather than the use of the most sophisticated analytical techniques.

# 12. Minimum Scope for the Academy

Roadway safety is a broad research field that cannot be fully explored within a single week. The purpose of this challenge is therefore not to develop a comprehensive safety model for Dallas County, but to experience the process of conducting transportation research using real-world data and modern analytical tools.

To keep the project both manageable and meaningful, the investigation should focus on a clearly defined research question and a limited number of comparable roadway environments.

At a minimum, the project should include:

- integration of **at least four** complementary datasets;
- a clearly defined methodology for identifying similar roadway locations;
- exploratory data analysis supported by maps and visualizations;
- comparison of several roadway locations with different crash occurrence;
- one interpretable statistical model;
- one machine-learning model;
- one explainable AI technique (such as SHAP or permutation importance);
- engineering interpretation of the results;
- discussion of limitations and uncertainty; and
- practical recommendations supported by evidence.

The emphasis should remain on understanding the transportation system rather than maximizing predictive accuracy or implementing the most advanced AI algorithms.

Projects that complete the minimum scope early may choose to extend the analysis by investigating crash severity, specific crash types, temporal patterns, additional datasets, or more advanced machine-learning methods. These extensions are entirely optional and are intended to encourage further exploration rather than increase the required workload.

Above all, this challenge should demonstrate how transportation engineering, data integration, and Artificial Intelligence can work together to investigate complex real-world problems. A successful project is one that develops a clear, well-supported explanation for why apparently similar roadway environments exhibit different crash occurrence and shows how those findings could contribute to safer transportation systems across Dallas County.
