# Research Challenge 4
# Why Do Some Intersections Experience More Crashes Than Similar Intersections?

---

# 1. Challenge Overview

Intersections are among the most complex and safety-critical components of a transportation network. Unlike roadway segments, where vehicles generally move in the same direction with relatively predictable interactions, intersections bring together multiple traffic streams, turning movements, pedestrians, cyclists, and transit vehicles within a confined space. Every vehicle entering an intersection must continuously make decisions regarding speed, lane position, right-of-way, and gap acceptance while interacting with numerous other road users. As a result, even small differences in intersection design or operation can have a significant influence on roadway safety.

Transportation agencies have long observed that intersections with apparently similar characteristics often experience very different crash occurrence. Two signalized intersections may carry comparable traffic volumes, have the same number of approach lanes, similar speed limits, and identical traffic control, yet one consistently experiences substantially more crashes than the other. Likewise, two stop-controlled intersections located within similar communities may exhibit remarkably different safety performance despite appearing nearly identical from a geometric perspective.

These observations suggest that intersection safety is influenced by far more than basic geometric design or traffic volume. Crash occurrence emerges from the interaction of traffic operations, turning movements, access management, signal control, surrounding land use, environmental conditions, driver behavior, and the broader transportation network. Some of these factors are directly measurable, while others remain hidden or difficult to quantify using publicly available datasets.

The objective of this challenge is to investigate why similar intersections exhibit different crash occurrence by integrating multiple transportation, infrastructure, environmental, and surrounding land-use datasets describing Dallas County. Rather than simply identifying crash hotspots, the goal is to develop an evidence-based explanation for the characteristics that are most strongly associated with elevated crash occurrence at intersections.

Artificial Intelligence and Machine Learning provide valuable analytical tools throughout this investigation. They can identify hidden relationships, discover nonlinear interactions, and help explain complex patterns within large transportation datasets. However, they serve as supporting tools rather than the primary objective of the project. Transportation engineering principles remain essential for interpreting analytical results and determining whether the discovered relationships represent meaningful safety mechanisms.

A useful way to frame this research challenge is:

> **After controlling for intersection geometry and traffic exposure, which operational, infrastructural, environmental, and surrounding land-use characteristics best explain why some intersections experience substantially more crashes than other physically similar intersections across Dallas County?**

Answering this question can help transportation agencies better understand intersection safety, prioritize engineering improvements, optimize traffic operations, and design safer intersections for all roadway users.

# 2. Why This Challenge Matters in Transportation

Although intersections occupy only a small portion of a transportation network, they are responsible for a disproportionately large share of traffic conflicts and crashes. Every day, thousands of vehicles, pedestrians, cyclists, buses, and freight vehicles converge at intersections where they must safely share limited space while following traffic control devices and responding to the actions of other road users. Because multiple traffic streams intersect at the same location, intersections naturally become some of the most complex operating environments within the transportation system.

Improving intersection safety is therefore a major priority for transportation agencies. Crashes occurring at intersections often involve crossing or turning movements, which can result in severe angle collisions, pedestrian injuries, bicycle crashes, and rear-end collisions caused by unexpected stopping or congestion. Even relatively minor operational deficiencies can significantly increase the likelihood of conflicts because drivers must make multiple decisions within a short period of time.

Historically, transportation agencies have identified hazardous intersections by examining historical crash records and ranking locations according to crash frequency or crash severity. While this approach is effective for identifying locations that require further investigation, it does not explain why certain intersections become persistent crash hotspots while other intersections with similar traffic volumes and geometric characteristics operate safely.

Modern transportation engineering increasingly seeks to answer that deeper question. Rather than responding only after crashes occur, agencies aim to identify the characteristics associated with elevated crash occurrence so that engineering improvements can be implemented proactively. This shift from reactive safety management to proactive safety management is one of the defining trends in contemporary transportation engineering.

Intersection safety is particularly important because many engineering improvements can be implemented without reconstructing the entire roadway. Changes such as signal timing optimization, protected turning phases, access management, improved pavement markings, enhanced lighting, pedestrian crossing improvements, or modifications to traffic control can often produce meaningful safety benefits while requiring significantly lower investment than major roadway reconstruction.

This challenge supports that proactive perspective by investigating how infrastructure, traffic operations, surrounding land use, accessibility, demographics, and environmental conditions interact to influence intersection safety. Rather than assuming that traffic volume or geometric design alone determine crash occurrence, the project examines intersections as components of a larger transportation system whose performance depends on many interacting factors.

The knowledge gained from this investigation has practical applications across transportation planning, traffic engineering, roadway design, and operations. Better understanding of intersection safety can help agencies prioritize investments, improve traffic control strategies, support Vision Zero initiatives, evaluate future intersection designs, and guide long-term transportation planning.

More broadly, this challenge illustrates how modern transportation engineering is becoming increasingly data-driven. Today, improving intersection safety requires integrating information from multiple datasets and combining engineering expertise with advanced analytical methods. Artificial Intelligence expands the ability to analyze these complex datasets, but meaningful safety improvements continue to depend on sound engineering interpretation and evidence-based decision making.

# 3. Why Finding the Answer Is Difficult

Understanding why some intersections experience substantially more crashes than others is considerably more challenging than simply comparing crash frequencies. Although intersections can often be described using variables such as traffic volume, number of approach lanes, or traffic control type, these characteristics alone rarely explain the full range of factors influencing intersection safety.

Unlike roadway segments, where vehicles generally travel in the same direction, intersections require multiple traffic streams to interact within a relatively small area. Through movements, left turns, right turns, pedestrians, cyclists, buses, and heavy vehicles all compete for space while operating under changing traffic control conditions. This complexity creates numerous opportunities for conflicts, making intersection safety one of the most difficult problems in transportation engineering.

One of the first challenges is that **traffic exposure differs among intersections**. A busy urban intersection naturally accommodates far more vehicle interactions than a lightly traveled suburban intersection. Consequently, comparing crash counts without considering traffic exposure can produce misleading conclusions. Traffic volumes, turning movements, and pedestrian activity must be considered before evaluating whether one intersection is genuinely less safe than another.

Another challenge is defining what makes two intersections **similar**. Two signalized intersections may have identical numbers of approach lanes and similar traffic volumes but differ in signal timing, turning movement proportions, nearby commercial activity, driveway density, or pedestrian demand. Likewise, two stop-controlled intersections may appear nearly identical while serving very different surrounding land uses or travel patterns. These subtle differences often have a significant influence on crash occurrence.

Intersection safety is also strongly affected by **traffic operations**, many of which change throughout the day. Queue formation, signal coordination, protected turning phases, cycle length, and fluctuations in traffic demand continuously influence how vehicles interact. An intersection that operates efficiently during off-peak periods may become considerably more hazardous during the morning or evening peak because of changing traffic patterns.

Human decision-making introduces another important source of uncertainty. Drivers approaching an intersection must judge gaps in opposing traffic, interpret signal indications, anticipate the actions of other road users, and react quickly to changing conditions. Decisions involving left turns, lane changes, yellow-light behavior, or yielding to pedestrians vary from driver to driver and cannot be fully captured using available transportation datasets.

Crash occurrence is further complicated by the fact that intersections experience **different types of crashes**, each with different contributing factors. Rear-end collisions are often associated with congestion and unexpected stopping, while angle crashes may result from signal violations, poor visibility, or inadequate gap acceptance. Pedestrian and bicycle crashes involve additional operational and infrastructure considerations. Consequently, a variable that helps explain one crash type may have little influence on another.

As with all transportation safety studies, **correlation should not be interpreted as causation**. A machine-learning model may identify commercial land use or intersection density as important explanatory variables, but these characteristics may simply represent more complex operational conditions such as higher turning volumes, greater pedestrian activity, or more frequent access points. Transportation engineering knowledge is therefore essential for interpreting analytical results correctly.

Finally, intersections should be viewed as components of a broader transportation network rather than isolated locations. Congestion, signal coordination, nearby intersections, transit operations, and surrounding roadway conditions all influence intersection performance. Understanding these network interactions is often just as important as understanding the characteristics of the intersection itself.

For these reasons, the objective of this challenge is not to identify one variable that explains intersection crashes. Instead, the goal is to understand how multiple transportation, operational, environmental, and community factors interact to influence intersection safety and to determine which of those factors are consistently associated with elevated crash occurrence across similar intersections.

# 4. Measurable Structural Factors and Hidden (Latent) Factors

Intersection safety is influenced by a wide range of interacting factors. Some of these factors can be measured directly using transportation and GIS datasets, while others remain hidden because they represent driver behavior, operational characteristics, or information that is difficult to collect consistently.

Separating these influences into **measurable structural factors** and **hidden (latent) factors** provides a useful framework for understanding what can realistically be analyzed using available data. Measurable factors form the foundation of quantitative analysis, whereas latent factors help explain why even well-designed models cannot account for every crash.

---

## Measurable Structural Factors

### Intersection Geometry

The physical design of an intersection strongly influences how road users interact.

Representative variables include:

- intersection type (signalized, stop-controlled, roundabout, etc.);
- number of approach lanes;
- exclusive turning lanes;
- lane widths;
- median configuration;
- channelized right turns;
- intersection angle;
- approach alignment; and
- nearby driveway spacing.

These characteristics determine the physical space available for vehicles and influence the number of potential conflict points.

---

### Traffic Operations

Traffic operations describe how the intersection functions during daily traffic conditions.

Representative variables include:

- approach traffic volume;
- turning movement proportions;
- Average Annual Daily Traffic (AADT);
- operating speed;
- queue formation;
- congestion level;
- heavy-vehicle percentage; and
- travel time reliability.

Operational characteristics frequently explain why intersections with similar geometry experience different safety performance.

---

### Traffic Control

Traffic control determines how conflicting traffic streams are managed.

Examples include:

- signal control type;
- stop control;
- protected left-turn phases;
- signal coordination;
- pedestrian signal phases;
- traffic signs; and
- pavement markings.

Although detailed signal timing data are often unavailable, the presence and type of traffic control remain important explanatory variables.

---

### Surrounding Land Use

The surrounding environment influences both traffic demand and the diversity of roadway users.

Representative variables include:

- commercial development;
- residential neighborhoods;
- schools;
- hospitals;
- shopping centers;
- employment density;
- parks; and
- mixed-use development.

These factors affect pedestrian activity, turning movements, delivery traffic, and the overall complexity of intersection operations.

---

### Accessibility and Connectivity

Intersections serve as connection points within the transportation network.

Useful variables include:

- roadway connectivity;
- intersection density;
- nearby transit stops;
- accessibility to major activity centers;
- proximity to freeway ramps; and
- surrounding roadway hierarchy.

Highly connected areas often experience more complex traffic patterns than isolated intersections.

---

### Demographic and Environmental Characteristics

Additional contextual variables include:

- population density;
- household income;
- commuting characteristics;
- vehicle ownership;
- rainfall;
- visibility;
- daylight conditions;
- time of day; and
- seasonal variation.

These variables influence travel demand, roadway use, and driving conditions but do not directly determine crash occurrence.

---

## Hidden (Latent) Factors

Several important contributors to intersection safety remain difficult to observe using publicly available datasets.

Examples include:

- driver gap acceptance;
- reaction time;
- distraction;
- aggressive driving;
- red-light running;
- yellow-light decision making;
- driver familiarity with the intersection;
- adaptive signal timing;
- temporary traffic control;
- queue spillback from nearby intersections;
- special events;
- emergency vehicle activity; and
- advanced driver-assistance systems.

Many of these factors vary continuously throughout the day and are rarely recorded at the network level.

---

## Why This Distinction Matters

Machine-learning models can only analyze the information available within the integrated datasets. Consequently, influential variables identified by the models should be interpreted as **observable indicators** rather than complete explanations of intersection safety.

For example, an analysis may conclude that commercial intersections experience higher crash occurrence. In reality, commercial land use may simply represent higher turning volumes, more driveway access, increased pedestrian activity, and greater operational complexity. Similarly, signalized intersections may appear less safe not because traffic signals increase crashes, but because signals are typically installed where traffic demand and conflict opportunities are already high.

Recognizing the difference between measurable and latent factors helps ensure that analytical results are interpreted appropriately. The objective is to identify meaningful relationships supported by the available evidence while acknowledging that some important contributors to intersection safety cannot be measured directly.

The strongest transportation studies combine quantitative analysis with engineering judgment, recognizing both the strengths and the limitations of the available data.

## Helper Functions That Support Measurable Factors

Several intersection-safety factors can be created with helper functions instead of being coded from scratch:

- `summarize_points_within_distance` for traffic signals, transit stops, signs, crashes, schools, hospitals, parks, employers, destinations, and nearby activity generators;
- `summarize_lines_within_distance` for nearby major roads, bikeways, trails, transit routes, freight corridors, and roadway hierarchy around intersections;
- `summarize_polygons_within_distance` for commercial development, residential neighborhoods, parks, school zones, development areas, and surrounding land-use context;
- `add_nearest_distance` for proximity to freeway ramps, major roads, transit stations, employment centers, and activity centers;
- `calculate_facility_coverage` for the share of surrounding areas covered by transit, bikeways, parks, school zones, or other facility buffers;
- `summarize_street_connectivity` for roadway connectivity, surrounding intersection density, road density, dead ends, links per node, and average segment length; and
- `calculate_land_use_mix` for mixed-use development after land-use area has been summarized by category.

# 5. How to Think About the Problem

A common approach to intersection safety analysis is to identify locations with the highest number of crashes and investigate what they have in common. While this can help identify crash hotspots, it often does not explain why some intersections experience substantially more crashes than others. High-crash intersections frequently differ in traffic demand, surrounding land use, roadway hierarchy, and operational characteristics, making direct comparison difficult.

This challenge follows a different approach.

Rather than beginning with the most hazardous intersections, the investigation should begin by identifying **intersections that are fundamentally similar** and then examining why their safety performance differs. By controlling for the major physical characteristics of an intersection, it becomes easier to identify additional factors that may contribute to higher crash occurrence.

The objective is therefore to develop an evidence-based explanation of intersection safety rather than simply producing a predictive model.

---

## Step 1: Define the Unit of Analysis

The first decision is selecting the intersection unit to be analyzed.

Depending on the available data, the analysis may focus on:

- individual intersections;
- signalized intersections only;
- stop-controlled intersections only; or
- specific intersection categories (such as four-leg or T-intersections).

Maintaining a consistent unit of analysis ensures that the integrated datasets remain comparable throughout the project.

---

## Step 2: Establish Intersection Similarity

The next step is to define what makes two intersections similar.

Representative similarity variables include:

- traffic control type;
- number of approaches;
- number of lanes;
- posted speed limits;
- approach traffic volume;
- roadway functional classification; and
- intersection configuration.

These variables describe the fundamental characteristics of an intersection before additional explanatory variables are considered.

Similarity can then be evaluated using clustering methods, nearest-neighbor approaches, or other distance-based techniques.

---

## Step 3: Select the Safety Outcome

Several measures of intersection safety are possible, including:

- total crash occurrence;
- injury crashes;
- severe crashes;
- rear-end crashes;
- angle crashes;
- pedestrian crashes; and
- bicycle crashes.

Selecting one primary outcome simplifies interpretation and provides a consistent objective for the investigation.

---

## Step 4: Integrate Supporting Datasets

After similar intersections have been identified, additional datasets should be integrated to describe the surrounding transportation environment.

Potential explanatory variables include:

- surrounding land use;
- roadway connectivity;
- nearby transit facilities;
- demographic characteristics;
- environmental conditions;
- access density;
- intersection spacing; and
- transportation infrastructure.

These datasets help explain differences that cannot be understood through intersection geometry alone.

---

## Step 5: Explore the Data

Exploratory analysis should precede predictive modeling.

Useful techniques include:

- descriptive statistics;
- intersection maps;
- scatter plots;
- comparison tables;
- spatial visualization; and
- correlation analysis.

Exploring the data often reveals patterns that guide feature selection and model development while also helping identify missing values or unusual observations.

---

## Step 6: Develop Analytical Models

Begin with an interpretable statistical model that provides a baseline understanding of the data.

Representative approaches include:

- Poisson Regression;
- Negative Binomial Regression; and
- Logistic Regression (for selected outcomes).

These models can then be compared with machine-learning approaches such as:

- Decision Trees;
- Random Forests;
- Gradient Boosting; or
- XGBoost.

Using both traditional and AI-based methods provides a more complete understanding of the relationships among variables.

---

## Step 7: Interpret the Results

The final stage of the analysis is interpretation.

Rather than asking which variable produced the highest feature importance score, consider questions such as:

- Are the results consistent across several similar intersections?

- Do the findings agree with established traffic engineering principles?

- Could an observed relationship be explained by an unmeasured operational factor?

- Are the conclusions useful for transportation agencies?

The strongest projects combine analytical evidence with engineering reasoning to develop practical recommendations.

Throughout the investigation, it is helpful to think like a transportation researcher rather than a machine-learning practitioner. Every analytical result should contribute to a broader explanation of how intersection design, operations, and surrounding conditions interact to influence crash occurrence.

Ultimately, the goal is not to discover a single cause of intersection crashes, but to identify combinations of factors that consistently explain why some intersections perform more safely than others.

# 6. Data That Can Help Answer the Challenge

Understanding intersection safety requires combining information from multiple sources because no single dataset can fully explain why crashes occur. Crash records identify **where** crashes happened and often describe **how** they occurred, but they rarely provide enough information to explain **why** one intersection consistently experiences more crashes than another with similar characteristics.

The objective of this challenge is therefore to integrate complementary datasets that describe the physical design, operational characteristics, surrounding environment, and travel demand associated with each intersection. Together, these datasets provide a more complete representation of the conditions that influence intersection safety.

---

## Available Data

### Intersection Crash Data

Crash records provide the primary outcome for this investigation. They identify crash locations, timing, severity, and crash characteristics, allowing comparisons among intersections throughout Dallas County.

Because this challenge focuses specifically on intersections, the crash dataset should first be filtered to include only intersection-related crashes.

---

### Roadway and Intersection Geometry

Roadway inventory and GIS datasets describe the physical characteristics of each intersection.

Representative information includes:

- intersection configuration;
- number of approach lanes;
- roadway classification;
- posted speed limits;
- turning lanes;
- median type; and
- approach geometry.

These variables provide the foundation for defining intersection similarity.

---

### Traffic Characteristics

Traffic datasets describe how each intersection operates under normal traffic conditions.

Examples include:

- Average Annual Daily Traffic (AADT);
- approach traffic volumes;
- average operating speed;
- congestion indicators;
- travel time; and
- speed variability.

These variables help account for traffic exposure and distinguish busy intersections from genuinely higher-risk locations.

---

### Transportation Infrastructure

Infrastructure datasets describe facilities that influence traffic movements and conflict management.

Representative variables include:

- traffic signals;
- stop control;
- pedestrian crossings;
- sidewalks;
- bicycle facilities;
- transit stops;
- roadway lighting; and
- traffic control devices.

These characteristics help explain how different intersection designs manage conflicting traffic streams.

---

### Land Use and Surrounding Environment

The environment surrounding an intersection strongly influences how it operates.

Useful datasets describe:

- commercial development;
- residential areas;
- schools;
- hospitals;
- shopping centers;
- employment centers;
- parks; and
- nearby activity generators.

Land use affects traffic demand, turning movements, pedestrian activity, and the diversity of roadway users approaching an intersection.

---

### Demographic and Mobility Data

Demographic information helps describe the communities served by each intersection.

Examples include:

- population density;
- household income;
- vehicle ownership;
- commuting characteristics;
- employment; and
- Origin–Destination (OD) travel patterns.

Although these variables do not directly determine crash occurrence, they provide valuable context regarding transportation demand and travel behavior.

---

### Environmental Data

Weather and environmental datasets provide additional information describing roadway operating conditions.

Examples include:

- rainfall;
- visibility;
- daylight conditions;
- temperature; and
- seasonal variation.

Environmental conditions often influence driver behavior and intersection operations, particularly during adverse weather.

---

## Data That Are Difficult to Obtain

Several important variables influencing intersection safety are not readily available within public transportation datasets.

Examples include:

- detailed turning movement counts;
- signal timing plans;
- protected turning phases;
- adaptive signal control data;
- queue lengths;
- gap acceptance behavior;
- red-light violations;
- pedestrian crossing volumes;
- bicycle volumes;
- connected-vehicle trajectories; and
- near-miss events.

These datasets would substantially improve intersection safety analysis but are typically available only through detailed traffic studies or agency traffic management systems.

---

## Why Missing Data Matter

The absence of these datasets does not prevent meaningful research, but it does influence how the results should be interpreted.

For example, if commercial intersections consistently exhibit higher crash occurrence, the underlying explanation may involve increased turning movements, driveway access, pedestrian activity, or delivery traffic rather than commercial development itself. Without direct measurements of these operational characteristics, machine-learning models can identify statistical relationships but cannot always distinguish among their underlying causes.

Consequently, the objective of this challenge is not to identify every factor influencing intersection safety. Instead, it is to develop the most complete explanation possible using the available evidence while recognizing that some important operational and behavioral variables remain unobserved.

Acknowledging these limitations is an essential part of responsible transportation research and helps ensure that engineering recommendations remain scientifically sound.

# 7. Where Does Artificial Intelligence and Machine Learning Fit?

Artificial Intelligence is **not** the objective of this research challenge. The objective is to understand why intersections with similar physical characteristics and traffic conditions experience different crash occurrence. AI and Machine Learning provide analytical tools that help investigate this question by identifying complex relationships, integrating multiple datasets, and supporting evidence-based transportation engineering decisions.

Intersection safety has traditionally been studied using statistical models such as **Poisson Regression** and **Negative Binomial Regression**, which remain the standard approaches for analyzing crash count data. These models are well understood, highly interpretable, and continue to play an important role in transportation safety research. However, modern intersections generate complex interactions among traffic operations, turning movements, pedestrians, cyclists, transit vehicles, and surrounding land uses. Capturing these nonlinear relationships often requires analytical techniques that extend beyond traditional statistical methods.

Machine learning complements these established approaches by providing additional tools for exploring complex transportation systems while preserving the need for engineering interpretation.

---

## How AI Can Support This Challenge

Artificial Intelligence can contribute at several stages of the investigation.

### Pattern Discovery

Before comparing crash occurrence, AI can help identify intersections with similar characteristics.

Representative techniques include:

- K-Means Clustering;
- Hierarchical Clustering;
- DBSCAN; and
- Principal Component Analysis (PCA).

These methods organize large datasets and identify comparable intersection environments that can later be investigated in greater detail.

---

### Feature Engineering

Many useful explanatory variables are not available directly from a single dataset but can be created by integrating multiple sources of information.

Examples include:

- intersection density;
- roadway connectivity;
- accessibility measures;
- surrounding land-use diversity;
- roadway complexity indices; and
- conflict opportunity indicators.

These derived features often describe intersection environments more effectively than individual raw variables.

---

### Predictive Modeling

Machine-learning models can estimate crash occurrence and identify variables associated with higher-risk intersections.

Representative models include:

- Decision Trees;
- Random Forests;
- Gradient Boosting;
- XGBoost; and
- LightGBM.

These methods are particularly effective for identifying nonlinear relationships and interactions among roadway geometry, traffic operations, infrastructure, and surrounding environmental conditions.

---

### Explainable AI

Transportation agencies must understand **why** an AI model reaches a particular conclusion before using that information to support engineering decisions.

Explainable AI techniques include:

- SHAP values;
- Permutation Importance;
- Partial Dependence Plots (PDP); and
- LIME.

These approaches help answer questions such as:

- Which intersection characteristics contribute most strongly to crash occurrence?

- How do traffic operations interact with roadway design?

- Do turning movements influence safety differently under different traffic conditions?

- Are there threshold effects associated with traffic volume or intersection complexity?

Rather than treating machine-learning models as black boxes, explainable AI transforms them into practical decision-support tools.

---

## Choosing the Appropriate Analytical Method

The most sophisticated model is not always the most useful.

Transportation agencies often prefer models that provide clear engineering insight rather than models that simply maximize predictive accuracy.

The following progression illustrates representative analytical methods that may be used throughout this challenge.

| Complexity | Representative Methods | Primary Purpose |
|------------|------------------------|-----------------|
| **Exploratory Analysis** | Correlation Analysis, PCA, Clustering | Explore the data and identify similar intersection environments. |
| **Baseline Statistical Models** | Poisson Regression, Negative Binomial Regression | Develop interpretable models for crash occurrence and establish a benchmark for comparison. |
| **Machine Learning** | Decision Trees, Random Forests, Gradient Boosting | Capture nonlinear relationships and interactions among intersection characteristics. |
| **Explainable AI** | SHAP, Permutation Importance, PDP, LIME | Interpret model behavior and quantify the influence of individual variables. |
| **Advanced Research Methods** | Graph Neural Networks (GNN), Graph Attention Networks (GAT), Causal AI | Model interactions among connected intersections and investigate advanced transportation research questions beyond the scope of this project. |

---

## AI and Transportation Engineering Work Together

Artificial Intelligence can identify patterns within large transportation datasets, but it cannot determine whether those patterns represent meaningful engineering mechanisms. Transportation engineering provides the theoretical foundation needed to interpret analytical results and translate them into practical recommendations.

For example, if a machine-learning model identifies high intersection density as an influential variable, engineering knowledge is required to determine whether that relationship reflects increased conflict points, complex traffic operations, or surrounding land-use characteristics. Likewise, if commercial activity appears strongly associated with crash occurrence, transportation engineering helps determine whether the relationship is actually driven by turning movements, pedestrian activity, driveway access, or another operational factor.

The strongest intersection safety studies combine the strengths of both disciplines. Machine learning discovers relationships that may otherwise remain hidden, while transportation engineering evaluates those relationships within the broader context of traffic operations, roadway design, and human behavior.

The objective is not to build the most advanced AI model. The objective is to use Artificial Intelligence responsibly to improve understanding of intersection safety and support better transportation decisions across Dallas County.

# 8. Recommended Analytical Workflow

The following workflow provides a structured approach for investigating why some intersections experience more crashes than other intersections with similar characteristics. While different analytical techniques may be used, the overall process should remain focused on developing transportation insight rather than simply building predictive models.

---

## Phase 1 – Define the Research Question

Begin by clearly defining the transportation problem.

Identify:

- the intersection type to be analyzed;
- the crash outcome of interest;
- the variables used to define intersection similarity; and
- the geographic scope of the study.

A clearly defined research question establishes the foundation for the entire investigation and helps maintain a consistent analytical focus.

---

## Phase 2 – Prepare and Integrate the Data

Collect and integrate datasets describing different aspects of each intersection.

Typical data sources include:

- intersection crash records;
- roadway inventory;
- traffic characteristics;
- transportation infrastructure;
- surrounding land use;
- demographic information;
- mobility data; and
- environmental conditions.

Before analysis, the datasets should be cleaned, standardized, and spatially joined so that every intersection is represented consistently across all data sources.

---

## Phase 3 – Explore the Data

Perform exploratory analysis to better understand the characteristics of the integrated dataset.

Useful techniques include:

- descriptive statistics;
- intersection maps;
- scatter plots;
- histograms;
- correlation matrices;
- comparison tables; and
- spatial visualizations.

Exploratory analysis often reveals meaningful relationships, identifies missing information, and guides later modeling decisions.

---

## Phase 4 – Develop and Compare Models

Develop an interpretable statistical model, such as Poisson Regression or Negative Binomial Regression, to establish a baseline understanding of crash occurrence.

Then develop one or more machine-learning models, such as Random Forest or Gradient Boosting, to investigate nonlinear relationships and interactions among the explanatory variables.

Rather than selecting a single "best" model, compare how different approaches explain the observed safety differences among similar intersections.

---

## Phase 5 – Interpret the Results

Use explainable AI techniques together with transportation engineering principles to interpret the analytical results.

Key questions include:

- Which variables consistently influence intersection safety?

- Are the relationships consistent across multiple intersections?

- Do the findings agree with established traffic engineering principles?

- Could hidden operational or behavioral factors explain part of the observed relationships?

This phase transforms statistical and machine-learning results into practical transportation knowledge.

---

## Phase 6 – Develop Engineering Recommendations

The final stage of the investigation is translating analytical findings into practical recommendations that transportation agencies could use to improve intersection safety.

Examples include:

- improving signal operations;
- redesigning turning movements;
- enhancing pedestrian facilities;
- improving access management;
- modifying intersection geometry;
- prioritizing future engineering studies; and
- identifying additional datasets that would strengthen future analyses.

The final outcome should not simply identify which intersections experience more crashes. It should explain **why** those differences occur and describe how the findings could contribute to safer intersection design, more effective traffic operations, and better transportation decision making across Dallas County.

# 9. Representative Research Papers

Intersection safety has been a major area of transportation research for many decades. Traditional studies primarily relied on statistical crash models to identify relationships between intersection characteristics and crash occurrence. More recent research has expanded this perspective by integrating machine learning, explainable Artificial Intelligence, computer vision, and network-based analysis to better understand the complex interactions that occur at intersections.

The following two representative studies illustrate how contemporary researchers investigate intersection safety and how modern analytical methods can complement traditional transportation engineering.

---

## Paper 1

### Li, J., Wang, X., Yang, X., Zhang, Q., & Pan, H. (2024)

**Analyzing Freeway Safety Influencing Factors Using the CatBoost Model and Interpretable Machine-Learning Framework (SHAP)**

*Transportation Research Record*

### Research Problem

Although this study focused primarily on freeway safety, its central research question is directly applicable to intersection safety:

> **How can machine-learning models improve transportation safety analysis while remaining interpretable enough for engineering decision making?**

The authors recognized that traditional statistical models often struggle to capture nonlinear relationships among roadway characteristics, while many advanced AI models function as black boxes that provide little engineering insight.

### Methodology

The researchers compared conventional statistical approaches with modern tree-based machine-learning models, including CatBoost. They then applied **SHAP (SHapley Additive Explanations)** to explain how individual variables contributed to model predictions.

### Key Findings

The study demonstrated that explainable machine learning could identify complex nonlinear relationships while maintaining sufficient transparency for transportation engineering applications. Rather than focusing solely on prediction accuracy, the framework helped explain why particular roadway characteristics influenced crash occurrence.

### Research Gap

The analysis concentrated primarily on roadway geometry and operational variables. Broader contextual information, including surrounding land use, accessibility, demographics, and multimodal transportation, was only partially represented.

### Future Research

The authors recommended integrating richer transportation datasets, expanding explainable AI methods, and applying these approaches to more diverse transportation environments.

### Relevance to This Challenge

The most important lesson from this paper is that Artificial Intelligence should support **understanding**, not simply prediction. This philosophy aligns directly with the objective of investigating why similar intersections exhibit different crash occurrence.

---

## Paper 2

### Abdel-Aty, M., Park, J., Lee, J., & Wang, J. (2023)

**A Machine Learning Framework for Identifying Contributing Factors to Intersection Crash Frequency**

*Accident Analysis & Prevention*

### Research Problem

The authors observed that intersections with similar traffic volumes and geometric characteristics frequently experience very different crash frequencies. They argued that traditional regression models often oversimplify these relationships because they assume relatively simple interactions among explanatory variables.

The study investigated whether machine-learning techniques could better identify the combinations of factors associated with elevated intersection crash occurrence.

### Methodology

Multiple intersection characteristics—including traffic exposure, geometric design, traffic control, and surrounding roadway conditions—were integrated into several machine-learning models. Explainable AI techniques were then used to evaluate feature importance and interpret the relationships identified by the models.

### Key Findings

The study demonstrated that intersection safety depends on the interaction of multiple variables rather than any single characteristic. Traffic volume, turning movements, signal control, surrounding roadway conditions, and geometric design all contributed to crash occurrence, but their influence varied depending on the overall operating environment.

### Research Gap

Although the models improved predictive performance, several operational variables remained unavailable, including detailed signal timing, driver behavior, pedestrian activity, and real-time traffic conditions. These missing variables limited the ability to fully explain intersection safety.

### Future Research

The authors suggested incorporating connected-vehicle data, high-resolution operational data, explainable AI techniques, and Digital Twin technologies to better understand how intersections operate under changing traffic conditions.

### Relevance to This Challenge

This study reinforces one of the central ideas of this project: intersection safety should be viewed as the result of interacting transportation, operational, and environmental factors rather than being explained by roadway geometry or traffic volume alone.

---

## Lessons from the Literature

Although these studies employ different analytical methods, they reach several common conclusions.

First, intersection safety cannot be explained by a single variable. Instead, crash occurrence emerges from the interaction of roadway design, traffic operations, infrastructure, land use, and human behavior.

Second, integrating multiple transportation datasets provides a more complete understanding of intersection safety than analyzing crash records alone.

Third, Artificial Intelligence is most valuable when it supports transportation engineering through interpretable models that help explain relationships rather than simply maximizing prediction accuracy.

Finally, both studies demonstrate that transportation engineering expertise remains essential. Machine learning can reveal complex patterns within large datasets, but engineering knowledge is required to determine whether those patterns represent meaningful safety mechanisms and to translate analytical findings into practical transportation improvements.

These lessons provide the scientific foundation for this research challenge and illustrate how data integration, explainable AI, and transportation engineering can work together to improve intersection safety across Dallas County.

# 10. How the Answer Can Improve Transportation Systems

The primary objective of this research challenge is not simply to identify intersections with high crash occurrence, but to develop a better understanding of **why** some intersections perform more safely than others despite having similar physical characteristics and traffic conditions. That understanding can help transportation agencies make more informed engineering decisions and improve safety before crashes become recurring problems.

Intersections are often among the most cost-effective locations for transportation improvements because relatively small operational or geometric changes can produce significant safety benefits. By identifying the factors that are consistently associated with elevated crash occurrence, agencies can move beyond reactive crash analysis and prioritize proactive engineering solutions.

The findings from this challenge may support a variety of transportation applications, including:

- prioritizing intersection safety improvements;
- optimizing traffic signal operations;
- improving left-turn and right-turn treatments;
- redesigning intersection geometry;
- enhancing pedestrian and bicycle crossings;
- improving access management near intersections;
- supporting Vision Zero initiatives; and
- guiding future intersection design standards.

Beyond individual engineering projects, this challenge demonstrates the importance of integrating multiple transportation datasets into a unified analytical framework. Combining crash records with roadway characteristics, traffic operations, land use, demographics, mobility, and environmental information provides a much more complete understanding of intersection safety than analyzing crash data alone.

The project also illustrates the complementary roles of Artificial Intelligence and transportation engineering. Machine-learning models can identify hidden relationships and complex interactions among variables, while engineering expertise provides the context needed to interpret those relationships and develop practical recommendations.

Ultimately, the value of this research is measured not by the sophistication of the analytical models, but by the quality of the transportation insight they produce. If the investigation helps explain why similar intersections experience different safety outcomes—and those findings can support safer intersection design, improved traffic operations, and more effective transportation planning—then the project has achieved its primary objective.

# 11. Expected Final Program Outcome

The objective of this research challenge is not to develop a production-ready intersection crash prediction model or to identify a single definitive cause of intersection crashes. Instead, the goal is to complete a structured transportation research investigation that integrates multiple datasets, applies appropriate analytical methods, and develops an evidence-based explanation for why similar intersections experience different crash occurrence.

By the conclusion of the project, the investigation should demonstrate how transportation engineering, data science, and Artificial Intelligence can work together to improve understanding of one of the most complex components of the transportation system.

A successful project should include:

- a clearly defined transportation research question;
- a reproducible methodology for identifying similar intersections;
- an integrated dataset representing multiple aspects of the transportation system;
- exploratory data analysis supported by appropriate visualizations;
- at least one interpretable statistical model;
- at least one machine-learning model;
- explainable AI results that help interpret the analytical findings;
- an engineering discussion of the results;
- a clear description of study limitations; and
- practical recommendations supported by evidence.

The final conclusions should focus on explaining **why** safety differences were observed rather than simply reporting prediction accuracy or feature importance rankings.

An example of an appropriate conclusion might be:

> Several signalized intersections with similar traffic volumes, roadway classifications, and geometric characteristics exhibited substantially different crash occurrence. After integrating roadway inventory, traffic operations, surrounding land use, demographic information, and environmental data, both statistical and machine-learning analyses consistently identified turning movement complexity, access density, nearby commercial activity, and operational characteristics as influential factors associated with elevated crash occurrence. Although detailed signal timing, turning movement counts, and driver behavior data were unavailable, the integrated analysis suggests that operational complexity plays a more significant role in explaining intersection safety than geometric similarity alone. These findings provide evidence that can support targeted engineering improvements and future transportation studies.

This example illustrates an important principle of transportation research: the objective is not to claim that one factor causes crashes, but to develop a well-supported explanation based on multiple independent sources of evidence.

Ultimately, the strongest projects will demonstrate thoughtful transportation reasoning, effective integration of diverse datasets, appropriate use of Artificial Intelligence, and practical engineering recommendations that could realistically assist transportation agencies in improving intersection safety.

# 12. Minimum Scope for the Academy

Intersection safety is one of the most active research areas in transportation engineering. Understanding why crashes occur requires combining roadway design, traffic operations, infrastructure, land use, environmental conditions, and human behavior into a single analytical framework. Completing a comprehensive study of every contributing factor would require extensive data collection and months of engineering analysis.

The objective of this challenge is therefore **not** to completely explain intersection safety across Dallas County. Instead, the goal is to experience the transportation research process by investigating a focused engineering question using real-world data and modern analytical techniques.

To keep the project both achievable and scientifically meaningful within the available time, the investigation should concentrate on a limited number of carefully selected intersections and develop a well-supported explanation for the observed differences in crash occurrence.

At a minimum, the project should include:

- integration of **at least four** complementary datasets;
- a clearly defined methodology for identifying similar intersections;
- exploratory data analysis supported by maps and visualizations;
- comparison of several similar intersections with different crash occurrence;
- one interpretable statistical model;
- one machine-learning model;
- one explainable AI technique (such as SHAP or permutation importance);
- engineering interpretation of the analytical findings;
- discussion of limitations and uncertainty; and
- practical recommendations supported by evidence.

The emphasis should remain on understanding **why** intersections perform differently rather than maximizing prediction accuracy or implementing the most sophisticated AI algorithms.

Projects that complete the minimum scope early may choose to extend the investigation by exploring:

- specific crash types (such as angle, rear-end, or pedestrian crashes);
- signalized versus stop-controlled intersections;
- temporal crash patterns;
- additional transportation datasets;
- advanced explainable AI methods;
- graph-based transportation models; or
- interactive dashboards for communicating engineering findings.

These extensions are entirely optional and are intended to encourage curiosity rather than increase the required workload.

Above all, this challenge should demonstrate how transportation engineering, data integration, and Artificial Intelligence can work together to investigate one of the most complex problems in urban transportation. A successful project is one that develops a clear, evidence-based explanation for why apparently similar intersections exhibit different safety performance and shows how those findings could support safer intersection design, improved traffic operations, and more informed transportation decision making across Dallas County.
