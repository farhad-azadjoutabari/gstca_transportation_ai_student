# Data Dictionary

This file summarizes the CSV datasets currently stored in `data/`. I inspected the CSV headers, sampled rows, and local README files where available. Several folders contain shapefiles, GeoJSON, or GeoPackage files in addition to CSV exports; the descriptions below focus on the CSV files because those are the files students are most likely to load in notebooks.

## Notes for Students

- `WKT` and `geometry` fields contain spatial geometry text, usually point or line geometry.
- `X` and `Y` fields are source GIS coordinates. They are not always longitude and latitude.
- `OBJECTID`, `fid`, `GIS_ID`, `COG_ID`, `GlobalID`, and similar fields are source-system identifiers.
- `Shape__Len`, `ShapeSTLen`, `Shape.STLength()`, `ShapeSTAre`, and similar fields are geometry measurements produced by GIS software.
- City of Dallas exports often include audit fields such as `created_us`, `created_da`, `last_edite`, `last_edi_1`, `CreationDa`, `Creator`, `EditDate`, and `Editor`. These describe when and by whom records were created or edited in the source system.
- Census `*-Data.csv` files are wide ACS tables. The first row contains coded column names, and the second row contains human-readable labels. When loading those files, skip or separately preserve the second row before converting numeric columns.

## `annual_average_daily_traffic_dallas_county_2024`

CSV file: `data/annual_average_daily_traffic_dallas_county_2024/csv/aadt_2024_dct.csv`

This Replica dataset describes 2024 annual average daily traffic on Dallas County road network links. It includes road segment identifiers, roadway attributes, geometry, total AADT, and truck AADT for single-unit and combination trucks where available.

- `stable_edge_id`: Replica stable road-network link identifier.
- `comp_stable_edge_id`: Matching stable edge identifier for the opposing direction, when the segment is bidirectional.
- `osm_id`: OpenStreetMap way identifier.
- `bidirectional`: Whether the traffic volume combines both directions on an undivided roadway.
- `compass_direction`: Direction of travel for the link.
- `street_name`: Street or road name from OpenStreetMap when available.
- `highway`: OpenStreetMap roadway classification.
- `length`: Link length in meters.
- `lanes`: Number of travel lanes.
- `heading`: Direction heading of the network link.
- `geometry`: Line geometry for the road segment.
- `aadt`: Annual average daily traffic volume.
- `aadt_single_unit`: Annual average daily single-unit truck volume; mainly populated for higher-class roads.
- `aadt_combination`: Annual average daily combination truck volume; mainly populated for higher-class roads.

## `bikeway_dallas_county`

CSV file: `data/bikeway_dallas_county/csv/bikeway_onstreet_existing.csv`

This dataset maps existing on-street bikeway facilities in Dallas County. It includes bikeway facility type, network category, status, name, and line geometry.

- `WKT`: Bikeway line geometry.
- `OBJECTID`: Source GIS record identifier.
- `Status`: Facility status, such as existing.
- `OnOffStr`: Whether the facility is on-street or off-street.
- `FuncClass`: Functional class of the associated street.
- `RegCorr`: Regional corridor flag or classification.
- `FacType`: Bikeway facility type, such as shared lane markings.
- `AlignPend`: Alignment-pending flag or field from the source layer.
- `Shape.STLength()`: GIS-computed line length.
- `StateNetCat`: State network category.
- `Name`: Facility or corridor name.
- `Source`: Source of the feature record.
- `Length`: Length value supplied by the source.

## `census_demographic_2024`

CSV files: one `*-Data.csv`, one `*-Column-Metadata.csv`, and one notes file per Census table folder.

These are 2024 ACS 5-year Census tract demographic tables for Dallas County. Each `*-Data.csv` is a wide table where rows are Census tracts and columns are ACS estimates and margins of error. Each matching `*-Column-Metadata.csv` maps the coded columns to human-readable labels.

Shared columns and patterns:

- `GEO_ID`: Census geography identifier.
- `NAME`: Census geography name.
- `...E`: ACS estimate column.
- `...M`: ACS margin-of-error column.
- `Column Name`: In metadata files, the coded ACS column name.
- `Label`: In metadata files, the full Census label for the coded column.

Included Census topic tables:

| Folder | Main data file | Columns | Topic |
| --- | --- | ---: | --- |
| `census_tract_age_and_sex_2024` | `ACSST5Y2024.S0101-Data.csv` | 459 | Age, sex, age categories, median age, dependency ratios |
| `census_tract_commuting_characteristics_by_sex_2024` | `ACSST5Y2024.S0801-Data.csv` | 345 | Workers, commute mode, travel time, vehicles, sex breakdowns |
| `census_tract_disability_characteristics_2024` | `ACSST5Y2024.S1810-Data.csv` | 417 | Disability status by sex, age, race, employment, and poverty |
| `census_tract_educational_attainment_2024` | `ACSST5Y2024.S1501-Data.csv` | 771 | Educational attainment by age, sex, race, and earnings |
| `census_tract_employment_status_2024` | `ACSST5Y2024.S2301-Data.csv` | 283 | Labor force, employment, unemployment, and participation |
| `census_tract_field_of_bachelor_degree_for_first_major_2024` | `ACSST5Y2024.S1502-Data.csv` | 291 | Field of bachelor's degree by sex, age, race, and earnings |
| `census_tract_housholds_and_families_2024` | `ACSST5Y2024.S1101-Data.csv` | 193 | Households, family types, children, and household size |
| `census_tract_income_in_past_12_months_2024` | `ACSST5Y2024.S1901-Data.csv` | 131 | Household income brackets and summary income measures |
| `census_tract_marital_status_2024` | `ACSST5Y2024.S1201-Data.csv` | 387 | Marital status by age and sex |
| `census_tract_means_of_transportation_to_work_by_selected_characteristic_2024` | `ACSST5Y2024.S0802-Data.csv` | 1013 | Commute mode by age, income, occupation, industry, and vehicle access |
| `census_tract_median_income_in_past_12_months_2024` | `ACSST5Y2024.S1903-Data.csv` | 243 | Median household income by race and household characteristics |
| `census_tract_poverty_status_in_past_12_month_2024` | `ACSST5Y2024.S1701-Data.csv` | 375 | Poverty status by age, sex, race, education, and employment |
| `census_tract_race_2024` | `ACSDT5Y2024.B02001-Data.csv` | 23 | Race counts and margins of error |
| `census_tract_school_enrollment_2024` | `ACSST5Y2024.S1401-Data.csv` | 411 | School enrollment by grade level, sex, age, and institution type |
| `census_tract_sex_of_workers_by_time_of_departure_to_go_to_work_2024` | `ACSDT5Y2024.B08011-Data.csv` | 93 | Workers by sex and departure-time interval |
| `census_tract_sex_of_workers_by_travel_time_to_work_2024` | `ACSDT5Y2024.B08012-Data.csv` | 81 | Workers by sex and commute travel-time interval |
| `census_tract_time_of_departure_to_go_to_work_2024` | `ACSDT5Y2024.B08302-Data.csv` | 33 | Workers by departure-time interval |

## `crosswalk_city_of_dallas`

CSV file: `data/crosswalk_city_of_dallas/csv/crosswalk.csv`

This City of Dallas traffic-control layer identifies crosswalk locations and related attributes such as school crosswalk status, signal association, striping schedule, and maintenance notes.

- `X`, `Y`: Crosswalk point coordinates.
- `OBJECTID`: Source GIS record identifier.
- `CWID`: Crosswalk identifier.
- `Mapsco`: Map grid reference.
- `FY_Striped`: Fiscal year when the crosswalk was striped.
- `FY_Schedul`: Fiscal year scheduled for work.
- `CouncilDis`: Council district.
- `Across_St`, `Street`, `Dir`: Street crossing and direction information.
- `CW`: Crosswalk type or crosswalk flag.
- `StopBar`: Stop-bar presence or status.
- `SchoolCW`: Whether the crosswalk is associated with a school.
- `Comment`, `Note`: Source comments and notes.
- `SignalCOGI`: Signal or COG intersection identifier.
- `Symb`, `ContCW`: Symbol/continuous-crosswalk classification fields.
- `SRNumber`: Service request number.
- `HIN`: High-injury-network indicator or related source flag.
- `StripedLas`: Last striped date or status.
- `AtSignal`: Whether the crosswalk is at a signal.
- `OtherFundi`: Other funding source indicator.
- `Schedule`, `ScheduleDa`: Scheduling status/date.
- `SchoolName`: Associated school name.
- `HL`: Highlight or source classification field.
- `Within1320`, `Within13_1`: Flags for proximity to a school or other buffered geography.
- `created_us`, `created_da`, `last_edite`, `last_edi_1`: Source edit audit fields.

## `dallas_dart_bus`

CSV files:

- `data/dallas_dart_bus/Dallas-DART-Route/csv/bus_route.csv`
- `data/dallas_dart_bus/Dallas-DART-Stops/csv/bus_stops.csv`

These datasets describe DART bus route alignments and stop locations.

Route columns:

- `WKT`: Route line geometry.
- `shape_id`: GTFS-style route shape identifier.
- `route_id`: DART route identifier.
- `route_shor`: Short route name or number.
- `route_long`: Long route name.
- `route_type`: Transit route type code.
- `route_colo`: Route display color.

Stop columns:

- `X`, `Y`: Stop point coordinates.
- `stop_name`: Public stop name.
- `stop_id`: DART stop identifier.

## `development_dallas_county`

CSV file: `data/development_dallas_county/csv/development.csv`

This regional point layer describes known development projects and facilities in Dallas County, including type, status, size, address, developer, and source fields.

- `X`, `Y`: Development point coordinates.
- `fid`, `OBJECTID`: Source record identifiers.
- `Name`: Development or facility name.
- `Type`, `SubClass`, `Class`: Feature type and classification.
- `Address`, `City`, `Zip`: Location address fields.
- `TEAID`, `Grades`: School-related identifiers/grade range when the record is a school.
- `DevType`, `DevStatus`: Development type and current development status.
- `SqFeet`, `Acreage`, `Beds`, `Doors`, `Units`, `Linear_Ft`, `Rooms`, `Seats`, `Students`: Size/capacity fields populated as applicable to the development type.
- `Completed`: Completion status or date field.
- `LastEdited`: Last source edit timestamp.
- `Phone`, `Website`: Contact or information fields.
- `StartDate`: Start date for the record or facility.
- `Developer`: Developer name.
- `DevLand`, `DevStyle`: Development land/style classification.
- `IsMixedUse`: Mixed-use indicator.
- `LEED`: Sustainability certification indicator.
- `Source`, `SourceDate`: Source name and source date.

## `dfw_mobility_level_of_congestion_2050`

No CSV file was found in this folder. The folder contains shapefile components and metadata for the 2050 mobility level-of-congestion layer. A CSV export would need to be created from the shapefile before students can load it with basic CSV readers.

## `dfw_truck_lane_restriction`

CSV file: `data/dfw_truck_lane_restriction/csv/truck_lane_restriction.csv`

This line layer identifies road segments with truck lane restrictions in the DFW region.

- `WKT`: Restricted segment line geometry.
- `OBJECTID`: Source GIS record identifier.
- `Facility`: Road or facility name.
- `From_Facil`, `To_Facilit`: From/to facility limits.
- `RestrStatu`: Restriction status.
- `ImplmntYr`: Implementation year.
- `ShapeSTLen`: GIS-computed segment length.

## `employers_dallas_county`

CSV file: `data/employers_dallas_county/csv/employer.csv`

This point layer lists major employers in Dallas County, including employer name, address, employment count, NAICS classification, and source date.

- `X`, `Y`: Employer point coordinates.
- `fid`: Source feature identifier.
- `EmpName`: Employer name.
- `EmpAddr`, `City`: Employer location.
- `Employees`: Number of employees.
- `NAICS`: Industry classification code.
- `StartDate`, `LastEdited`: Source record dates.
- `EmpID`: Employer identifier.
- `MailAddr`, `MailCity`, `MailZip`: Mailing address fields.
- `SourceDate`: Date of source information.
- `FeatureNam`: Feature name.
- `ActivitySe`: Activity sector or source activity classification.

## `ev_charging_stations_dallas_county`

CSV file: `data/ev_charging_stations_dallas_county/csv/ev_charging_stations.csv`

This point layer describes EV charging stations in Dallas County, including network, location, and plug counts.

- `X`, `Y`: Station point coordinates.
- `fid`, `recid`, `ESRI_OID`: Source record identifiers.
- `Station_Na`: Station name.
- `City`, `Street_Add`, `ZIP`: Station address.
- `ev_connect`: EV connector or access field.
- `ev_network`, `ev_netwo_1`: Charging network fields.
- `Level1_Plu`, `Level2_Plu`, `DCFC_Plugs`, `Total_Plug`: Plug counts by charging level and total.
- `Level2`, `DCFC`, `Tesla`: Charging capability flags.

## `existing_airport_dfw`

CSV file: `data/existing_airport_dfw/csv/airports.csv`

This polygon/area layer describes existing airports in the DFW area, including ownership, airport type, runway information, and services.

- `WKT`: Airport area geometry.
- `OBJECTID`: Source GIS record identifier.
- `AirportNam`: Airport name.
- `FAA_ID`: FAA airport identifier.
- `Commercial`, `GeneralAvi`, `Military`, `CAP`: Airport-use category flags.
- `Access`: Access classification.
- `OnSiteFire`: On-site fire service indicator.
- `Paved`: Paved runway indicator.
- `Tower`: Control tower indicator.
- `Customs`: Customs service indicator.
- `Owner`: Airport owner.
- `YearOpened`: Opening year.
- `LongestRun`: Longest runway length.
- `RunwaySour`: Runway data source.
- `Informatio`: Additional information field.
- `ShapeSTAre`, `ShapeSTLen`: GIS-computed area and perimeter.

## `features_dallas_county`

CSV file: `data/features_dallas_county/csv/features.csv`

This point layer contains regional features and community facilities such as schools or other points of interest. It includes classification, address, contact, source, and student fields where applicable.

- `X`, `Y`: Feature point coordinates.
- `fid`, `OBJECTID`: Source identifiers.
- `Name`: Feature name.
- `Type`, `SubClass`, `Class`: Feature category fields.
- `Address`, `City`, `Zip`: Location fields.
- `StartDate`, `LastEdited`: Source record dates.
- `TEAID`, `Grades`, `Students`: School-related fields when applicable.
- `Phone`, `Website`: Contact or information fields.
- `Notes`: Source notes.
- `Source`, `SourceDate`: Source name and source date.

## `flashers_city_of_dallas`

CSV file: `data/flashers_city_of_dallas/csv/flasher.csv`

This City of Dallas point layer describes school flashers and related traffic-control equipment near schools.

- `X`, `Y`: Flasher point coordinates.
- `OBJECTID`: Source GIS record identifier.
- `Site`, `SCHOOL`, `TYPSCH`: School/site name and school type.
- `STREET`, `ADDRESS`, `MAPSCO`, `Direction`: Location and map reference fields.
- `Notes`: Source notes.
- `FLASHID`, `ZONEID`, `GISID`: Flasher, zone, and GIS identifiers.
- `SOLAR`: Solar-powered indicator.
- `HEADS`: Number of signal heads.
- `Councils`: Council district field.
- `DeviceType`: Type of flasher/device.
- `MaintbyTRN`: Whether maintained by Transportation.
- `Fl_Status`: Flasher status.
- `InTOD`, `OnPHIN`, `InPIZ`, `PIZ`: Source program or geography flags.
- `CityArea`: City area classification.
- `TruckRoute`: Truck-route flag.
- `THPFunctio`: Thoroughfare plan function or similar road classification.
- `SpeedLimit`: Posted speed limit.
- `Installati`, `InstalYear`: Installation date/year.
- `created_us`, `created_da`, `last_edite`, `last_edi_1`, `CreationDa`, `Creator`, `EditDate`, `Editor`: Source edit audit fields.

## `free_flow_speed_dallas_county_2024`

CSV file: `data/free_flow_speed_dallas_county_2024/csv/annual-speeds_2024_dct.csv`

This Replica road-link dataset reports annual speed summaries for Dallas County. The README defines free-flow speed as the 66th percentile speed during off-peak hours.

- `stable_edge_id`: Replica road-network link identifier.
- `osm_id`: OpenStreetMap way identifier.
- `compass_direction`: Direction of travel.
- `street_name`: Street name from OpenStreetMap when available.
- `highway`: OpenStreetMap roadway classification.
- `length`: Link length in meters.
- `lanes`: Number of travel lanes.
- `heading`: Direction heading.
- `geometry`: Line geometry for the road link.
- `average_speed_mph`: Annual average speed in miles per hour.
- `free_flow_speed_mph`: Free-flow speed in miles per hour.
- `speed_p50_mph`: Median speed in miles per hour.
- `speed_p85_mph`: 85th percentile speed in miles per hour.
- `speed_p95_mph`: 95th percentile speed in miles per hour.

## `freight_dallas_county`

CSV files: eight FAF5 truck-flow tables for 2022 and 2050 base-year scenarios, split by domestic, export, import, and total/all truck flows.

These files describe truck freight flows by highway network link and commodity class. Each file has the same structure: an `ID` link identifier and directional/total measures of truck trips and tons.

Shared column pattern:

- `ID`: Highway network link identifier.
- `AB ...`: Directional flow from network node A to node B.
- `BA ...`: Directional flow from network node B to node A.
- `TOT ...`: Total two-way flow.
- `Tons`: Freight tonnage.
- `Trips`: Truck trip count.
- `_22`: 2022 scenario suffix.
- `_50Base`: 2050 base scenario suffix.
- `Dom`, `Exp`, `Imp`, `All`: Domestic, export, import, or total/all flow type.

Commodity groups represented in the headers:

- `Farm Products`
- `Food, Bev and Tobacco`
- `Stone Sand Gravel & Ores`
- `Liquid and Gases`
- `Chemicals`
- `Logs & Oth Wood Prods`
- `Waste and Scrap`
- `Consumer Manuf`
- `Durable Manuf (low tech)`
- `Durable Manuf (high tech)`
- `Motor and Other Veh`
- `Mixed Freight`

## `historical_crash_data`

CSV files:

- `data/historical_crash_data/intersection-related-crash-data-DallasCounty-2024.csv`
- `data/historical_crash_data/speed-related-crash-data.csv`

These TxDOT crash exports contain reportable 2024 Dallas County crashes. Both files have a preamble before the header and then share the same 260-column schema. The intersection file is filtered to intersection-related crashes; the speed file is filtered to speed-related crashes. A single crash can appear on multiple rows because unit/person records repeat the same crash-level fields.

Important column groups:

- Crash identifiers: `Crash ID`, `Case ID`, `Crash Number`.
- Crash date/time: `Crash Date`, `Crash Month`, `Crash Time`, `Crash Year`, `Day of Week`, `Hour of Day`.
- Location: `County`, `City`, `Street Name`, `Street Number`, `Latitude`, `Longitude`, `Intersecting Street Name`, `Intersecting Highway Number`, `Reference Marker Number`, `Reference Marker Offset Distance`.
- Severity and injuries: `Crash Severity`, `Fatal Crash Flag`, `Crash Death Count`, `Crash Total Injury Count`, `Crash Possible Injury Count`, `Crash Suspected Serious Injury Count`, `Crash Non-Suspected Serious Injury Count`, `Crash Not Injured Count`, `Crash Unknown Injury Count`.
- Road context: `Road Class`, `Roadway Type`, `Roadway Part`, `Roadway Relation`, `Roadway Alignment`, `Roadway Function`, `Roadbed Type`, `Number of Lanes`, `Speed Limit`, `Surface Type`, `Surface Width`, `Median Type`, `Median Width`, `Shoulder` fields.
- Traffic and environment: `Traffic Control Type`, `Light Condition`, `Weather Condition`, `Surface Condition`, `Construction Zone Flag`, `School Bus Flag`, `Active School Zone Flag`, `At Intersection Flag`, `Intersection Related`.
- Crash events and factors: `First Harmful Event`, `Manner of Collision`, `Object Struck`, `Contributing Factors`, `Contributing Factor 1`, `Contributing Factor 2`, `Contributing Factor 3`, `Other Factor`, `Possible Contributing Factor 1`, `Possible Contributing Factor 2`.
- Administrative fields: `Agency`, `Investigation Complete`, `TxDOT Reportable Flag`, `MPO`, `Region`, `ORI Number`, `On System Flag`, `Toll Road Flag`.
- Commercial vehicle fields: columns beginning with `CMV`, plus `Commercial Motor Vehicle Flag`, `Carrier's Primary Address - Zip`, `Ten Thousand Lbs Flag`, `Transporting Hazardous Material Flag`.
- Unit and vehicle fields: `Unit Number`, `Unit Description`, `Vehicle Body Style`, `Vehicle CMV Flag`, `Vehicle Color`, `Vehicle Damage Rating...`, `Vehicle Defect...`, `Vehicle Make`, `Vehicle Model Name`, `Vehicle Model Year`, `Vehicle Parked Flag`, `Vehicle Travel Direction`, `VIN`.
- Driver fields: `Driver License Class`, `Driver License State`, `Driver Zip Code`, `Driver Alcohol Result`, `Driver Drug Test Result`, `Driver Blood Alcohol Content Test Result`, `Financial Responsibility Proof`.
- Person fields: `Person Number`, `Person Type`, `Person Age`, `Person Gender`, `Person Ethnicity`, `Person Injury Severity`, `Person Restraint Used`, `Person Airbag Deployed`, `Person Ejected`, `Physical Location of An Occupant`.
- Emergency response fields: `Date Notified`, `Date Arrived`, `Date Roadway Cleared`, `Date Scene Cleared`, `Time Notified`, `Time Arrived`, `Time Roadway Cleared`, `Time Scene Cleared`, `Nearest Trauma Center`, `Nearest Trauma Center Distance`.

Note: These files include potentially sensitive vehicle/person fields such as `VIN`, `Driver Zip Code`, and `Lessee/Owner Zip Code`. Consider dropping or masking those before student exercises.

## `historical_weather_data`

CSV file: `data/historical_weather_data/DallasCounty-Weather-Data-2024.csv`

This NOAA-style daily weather dataset contains 2024 observations for weather stations in Dallas County. Many fields are sparse because different stations report different measurement types.

- `STATION`: Weather station identifier.
- `NAME`: Weather station name.
- `DATE`: Observation date.
- `AWND`: Average daily wind speed.
- `DAPR`: Number of days represented in a multi-day precipitation total.
- `EVAP`: Evaporation measurement, when reported.
- `MDPR`: Multi-day precipitation amount.
- `MNPN`, `MXPN`: Evaporation-pan minimum/maximum fields, when reported.
- `PGTM`: Peak gust time.
- `PRCP`: Precipitation amount.
- `SNOW`: Snowfall amount.
- `SNWD`: Snow depth.
- `TAVG`: Average temperature.
- `TMAX`: Maximum temperature.
- `TMIN`: Minimum temperature.
- `TOBS`: Temperature at observation time.
- `WDF2`, `WDF5`: Direction of fastest 2-minute and 5-second wind.
- `WSF2`, `WSF5`: Speed of fastest 2-minute and 5-second wind.
- `WT01` to `WT09`: Weather-type flags, such as fog, thunder, ice pellets, hail, glaze, dust/ash, smoke/haze, or blowing snow.

## `hourly_speed_dallas_county_2024`

CSV files:

- `AverageSpeed/csv/qtr-hourly-speeds_2024_dct.csv`
- `MedianSpeed/csv/qtr-hourly-speeds_2024_dct.csv`
- `Percentile85/csv/qtr-hourly-speeds_2024_dct.csv`

These Replica files describe quarter-hourly weekday speed profiles for road links. The three folders share the same schema but report different speed metrics: average speed, median/P50 speed, and P85 speed.

- `stable_edge_id`: Replica road-network link identifier.
- `osm_id`: OpenStreetMap way identifier.
- `compass_direction`: Direction of travel.
- `street_name`: Street name from OpenStreetMap when available.
- `highway`: Roadway classification.
- `length`: Link length in meters.
- `lanes`: Number of lanes.
- `heading`: Link heading.
- `geometry`: Line geometry.
- `free_flow_speed_mph`: Free-flow speed in miles per hour.
- `wkdy_0000` through `wkdy_2345`: Speed value for each weekday quarter-hour time bin.

## `hourly_traffic_volume_dallas_county_2024`

CSV files:

- `HeavyTruck/csv/hourly-volumes_2024_dct.csv`
- `MediumTruck/csv/hourly-volumes_2024_dct.csv`
- `Total/csv/total-hourly-volume-dallas-county-2024.csv`

These Replica files describe hourly weekday traffic volumes by road link. The heavy-truck file reports combination-truck volume, the medium-truck file reports single-unit truck volume, and the total file reports all-vehicle volume.

- `stable_edge_id`: Replica road-network link identifier.
- `comp_stable_edge_id`: Opposing-direction link identifier when relevant.
- `osm_id`: OpenStreetMap way identifier.
- `bidirectional`: Whether values combine both directions.
- `compass_direction`: Direction of travel.
- `street_name`: Street name.
- `highway`: Roadway classification.
- `length`: Link length in meters.
- `lanes`: Number of lanes.
- `heading`: Link heading.
- `geometry`: Line geometry.
- `aadt`: Annual average daily traffic for total-volume file.
- `aadt_single_unit`: Annual average daily single-unit truck volume for medium-truck file.
- `aadt_combination`: Annual average daily combination truck volume for heavy-truck file.
- `wkdy_0` through `wkdy_23`: Hourly weekday volume by hour of day.

## `lan_use_dallas_county`

CSV files:

- `BuildingArea/csv/land-use_fall-2024_dct.csv`
- `LandArea/csv/land-use_fall-2024_dct.csv`

These Replica land-use tables summarize 2024 land use by Census geography. One file reports building area by category; the other reports land area by category.

Shared columns:

- `geo_fips`: Census geography FIPS code.
- `name`: Geography name.

Building-area columns:

- `building_area_single_family`: Building area used for single-family residential.
- `building_area_multi_family`: Building area used for multifamily residential.
- `building_area_retail`: Retail building area.
- `building_area_office`: Office building area.
- `building_area_non_retail_attraction`: Commercial attraction building area that is not retail.
- `building_area_industrial`: Industrial building area.
- `building_area_civic_institutional`: Civic/institutional building area.
- `building_area_healthcare`: Healthcare building area.
- `building_area_education`: Education building area.
- `building_area_transportation_utilities`: Transportation and utilities building area.
- `building_area_open_space`: Open-space building area category.
- `building_area_agriculture`: Agriculture building area.
- `building_area_other`: Other building area.
- `building_area_unknown`: Unknown building area.

Land-area columns:

- `land_area_single_family`: Land area used for single-family residential.
- `land_area_multi_family`: Land area used for multifamily residential.
- `land_area_retail`: Retail land area.
- `land_area_office`: Office land area.
- `land_area_non_retail_attraction`: Commercial attraction land area that is not retail.
- `land_area_mixed_use`: Mixed-use land area.
- `land_area_industrial`: Industrial land area.
- `land_area_civic_institutional`: Civic/institutional land area.
- `land_area_healthcare`: Healthcare land area.
- `land_area_education`: Education land area.
- `land_area_transportation_utilities`: Transportation and utilities land area.
- `land_area_open_space`: Open-space land area.
- `land_area_agriculture`: Agriculture land area.
- `land_area_other`: Other land area.
- `land_area_unknown`: Unknown land area.

## `on_demand_transit_zone_dfw`

No CSV file was found in this folder. The folder contains shapefile components for on-demand transit zones. A CSV or GeoJSON export would be useful if students need to work with this dataset in basic notebook exercises.

## `origin_destination_trip_table_dallas_county_2024`

CSV files: `part1` through `part4`, each with the same 43-column schema.

This Replica trip table describes individual or modeled trips involving Dallas County tracts for Fall 2024 Thursday travel. The table is split into four large parts. It includes origin/destination Census geographies, trip timing, mode, purpose, vehicle information, and trip-taker demographic attributes.

- `activity_id`: Unique trip/activity record identifier.
- `origin_bgrp_2020`, `origin_trct_2020`: Origin Census block group and tract.
- `destination_bgrp_2020`, `destination_trct_2020`: Destination Census block group and tract.
- `primary_mode`: Primary travel mode.
- `trip_purpose`: Purpose of the current trip.
- `previous_trip_purpose`: Purpose of the previous trip.
- `trip_start_time`, `trip_end_time`: Trip start/end timestamps or time bins.
- `trip_duration_minutes`: Trip duration in minutes.
- `trip_distance_miles`: Trip distance in miles.
- `vehicle_type`: Vehicle type used for the trip, when relevant.
- `vehicle_fuel_type`: Vehicle fuel type, when relevant.
- `origin_land_use`, `origin_building_use`: Origin land/building use.
- `destination_land_use`, `destination_building_use`: Destination land/building use.
- `trip_taker_age`: Trip taker age.
- `trip_taker_sex`: Trip taker sex.
- `trip_taker_race_ethnicity`: Trip taker race/ethnicity category.
- `trip_taker_employment_status`: Employment status.
- `trip_taker_wfh`: Work-from-home status.
- `trip_taker_individual_income`: Individual income category.
- `trip_taker_commute_mode`: Usual commute mode.
- `trip_taker_household_size`: Household size.
- `trip_taker_household_income`: Household income category.
- `trip_taker_available_vehicles`: Available vehicles in household.
- `trip_taker_resident_type`: Resident type.
- `trip_taker_industry`: Worker industry.
- `trip_taker_building_type`: Home building type.
- `trip_taker_school_grade_attending`: School grade attended.
- `trip_taker_education`: Educational attainment.
- `trip_taker_tenure`: Housing tenure.
- `trip_taker_language`: Language category.
- `trip_taker_home_bgrp_2020`, `trip_taker_home_trct_2020`, `trip_taker_home_cty_2020`, `trip_taker_home_st_2020`: Home block group, tract, county, and state.
- `trip_taker_work_bgrp_2020`, `trip_taker_work_trct_2020`, `trip_taker_work_cty_2020`, `trip_taker_work_st_2020`: Work block group, tract, county, and state.

## `parks_dallas_county`

CSV file: `data/parks_dallas_county/csv/parks.csv`

This polygon layer describes parks in Dallas County, including ownership, city, status, source, and area fields.

- `WKT`: Park geometry.
- `fid`, `OBJECTID`: Source identifiers.
- `NAME`: Park name.
- `OWNER`: Owner or managing entity.
- `NOTES`: Source notes.
- `CITY`: City where the park is located.
- `FEATTYPE`: Feature type.
- `STATUS`: Park status.
- `SOURCE`, `SOURCE_YEA`: Source and source year.
- `ShapeSTLen`, `ShapeSTAre`: GIS-computed perimeter/area.
- `AREA`: Area value from source.

## `rail_stations_dallas_county`

CSV file: `data/rail_stations_dallas_county/csv/rail_station.csv`

This point layer describes rail stations in Dallas County, including name, classification, address, contact, source, and last-edited fields.

- `X`, `Y`: Station point coordinates.
- `fid`, `OBJECTID`, `FeatureID`, `TypeID`: Source identifiers.
- `Name`: Station name.
- `Type`, `Class`, `SubClass`: Station classification.
- `Address`, `City`, `Zip`: Location address fields.
- `Phone`, `Website`: Contact/information fields.
- `StartDate`: Source start/opening date field.
- `Source`, `SourceDate`: Source name and date.
- `LastEdited`: Last source edit timestamp.

## `roads_dallas_county`

No CSV file was found in this folder. The folder contains GeoPackage files for OSM roadway classes: `motorway`, `primary`, `secondary`, and `tertiary`. These could be exported to CSV/GeoJSON if students need road attributes in a notebook without geospatial file readers.

## `school_zones_city_of_dallas`

CSV file: `data/school_zones_city_of_dallas/csv/school_zone.csv`

This City of Dallas line layer describes school speed zones and related flasher/school information.

- `WKT`: School-zone line geometry.
- `OBJECTID`: Source GIS record identifier.
- `GIS_ID`: School-zone GIS identifier.
- `FLSHID1`, `FLSHID2`, `FLASHERS`: Associated flasher identifiers/count/status.
- `MAPSCO`: Map grid reference.
- `StreetName`, `BlockCO`, `ExtentCO`: Street and zone extent fields.
- `School`: Associated school name.
- `Councils`: Council district field.
- `Comment`, `Note`: Source comments/notes.
- `OrdinDate`, `OrdinNumbe`: Ordinance date and number.
- `Engineer`: Responsible engineer field.
- `SpeedLimit`: Posted school-zone speed limit.
- `TPFunction`: Thoroughfare plan or roadway function.
- `Divided`: Whether the street is divided.
- `Lanes`: Number of lanes.
- `ChangestoC`: Change-to-code or change-status source field.
- `Status`: Zone status.
- `created_us`, `created_da`, `last_edite`, `last_edi_1`, `CreationDa`, `Creator`, `EditDate`, `Editor`: Source edit audit fields.
- `Shape__Len`: GIS-computed line length.

## `signalized_intersections_city_of_dallas`

CSV file: `data/signalized_intersections_city_of_dallas/csv/signalized_intersections.csv`

This point layer describes signalized intersections in Dallas, including signal type, intersection name, street names, council district, retiming fields, and speed/classification fields.

- `X`, `Y`: Signal point coordinates.
- `OBJECTID`: Source GIS record identifier.
- `GIS_ID`, `COG_ID`: City and COG signal/intersection identifiers.
- `SIGNALTYPE`: Signal type.
- `INTERSNAME`, `NAME2`: Intersection name fields.
- `MAPSCO`: Map grid reference.
- `StreetEW`, `StreetNS`: East-west and north-south street names.
- `CouncilDis`: Council district.
- `Retiming`: Signal retiming status/field.
- `Class1_TXD`, `Class2_TXD`: TxDOT classification fields for intersecting roads.
- `SpeedL1`, `SpeedL2`: Speed limits for intersecting roads.
- `SignalDist`: Signal district.
- `created_us`, `created_da`, `last_edite`, `last_edi_1`, `CreationDa`, `Creator`, `EditDate`, `Editor`: Source edit audit fields.

## `signal_cabinet_city_of_dallas`

CSV file: `data/signal_cabinet_city_of_dallas/csv/signal_cabinet.csv`

This point layer describes signal cabinets and equipment at signalized intersections.

- `X`, `Y`: Cabinet point coordinates.
- `fid`, `OBJECTID`: Source identifiers.
- `GIS_ID`, `COG_ID`: City and COG signal identifiers.
- `SIGNALTYPE`: Signal type.
- `INTERSNAME`: Intersection name.
- `MAPSCO`: Map grid reference.
- `ONSYSTEM`, `TXDOTSYST`, `SignalSystem`: System ownership or signal-system fields.
- `StreetEW`, `StreetNS`: Intersecting street names.
- `CouncilDistrict`: Council district.
- `HSIPYear`, `HSIPLettingYear`, `HSIPProjNumber`: Highway Safety Improvement Program fields.
- `ITSCorrName`: ITS corridor name.
- `Address`: Cabinet/intersection address.
- `StatusDate`: Status date.
- `Contractor`: Contractor name.
- `Controller`, `ConflictMonitor`, `Cabinet`, `Poles`, `LumPoles`, `LumInstalled`: Signal equipment fields.
- `VehDetection`, `DetEquip`, `DetEquipInstDate`: Vehicle detection equipment and installation date.
- `BBUInstDate`: Battery backup installation date.
- `SignalStatus`: Signal status.
- `FlashTestDate`, `YellowFlashStreet`, `NightFlash`: Flashing-operation fields.
- `ATC_InstallDate`, `ATC_Instal_Year`: Advanced traffic controller installation fields.
- `Note`: Source notes.
- `AssetDataSource`: Source of asset data.
- `FiberinCabinet`: Fiber connection indicator.
- `MapField`: Mapping field.
- `CabinetInstDate`: Cabinet installation date.
- `CameraEquip`, `Number_Cameras`: Camera equipment and count.
- `created_user`, `created_date`, `last_edited_user`, `last_edited_date`, `CreationDate`, `Creator`, `EditDate`, `Editor`: Source edit audit fields.

## `signal_projects_city_of_dallas`

CSV file: `data/signal_projects_city_of_dallas/csv/signal_projects.csv`

This point layer describes signal projects in Dallas, including project type, status, funding, manager contact, and schedule dates.

- `X`, `Y`: Project point coordinates.
- `OBJECTID`: Source GIS record identifier.
- `GIS_ID`, `COG_ID`: Signal/intersection identifiers.
- `SIGNALTYPE`: Signal type.
- `SIGNALNAME`: Signal or intersection name.
- `MAPSCO`: Map grid reference.
- `COUNCIL`: Council district.
- `PR_TYPE`: Project type.
- `CONTRACTOR`: Contractor.
- `PR_STATUS`: Project status.
- `LETTING_DA`: Letting date.
- `COMMENT`: Source comments.
- `PROJECT_NA`: Project name.
- `EST_COMPLE`: Estimated completion.
- `PM_NAME`, `PM_PHONE`, `PM_EMAIL`: Project manager contact fields.
- `DEPARTMENT`: Responsible department.
- `LOCATION`: Project location description.
- `AWARD_DATE`: Award date.
- `ACT_COMPLE`: Actual completion date.
- `PR_FUNDING`: Project funding source.
- `MAP_LABEL`: Map display label.
- `CreationDa`, `Creator`, `EditDate`, `Editor`: Source edit audit fields.

## `speed_limits_city_of_dallas`

CSV file: `data/speed_limits_city_of_dallas/csv/speed_limit.csv`

This line layer describes City of Dallas speed-limit segments, including street names, from/to limits, lane count, truck route indicator, and ordinance fields.

- `WKT`: Speed-limit segment geometry.
- `OBJECTID`: Source GIS record identifier.
- `MAJORST_ID`: Major street identifier.
- `STNAME`, `STPRE`, `STYPE`, `STSUFX`: Street-name components.
- `FROM_ST`, `TO_ST`: Segment limits.
- `TPLINK`, `SEC`: Source link/section fields.
- `NRLANES`: Number of lanes.
- `OPER`: Operation or directionality field.
- `TRUCK_RT`: Truck-route indicator.
- `SPEEDLIM`: Posted speed limit.
- `CONFIG`: Street configuration.
- `OrdinNumbe`, `OrdinDate`: Ordinance number and date.
- `created_us`, `created_da`, `last_edite`, `last_edi_1`: Source edit audit fields.
- `Shape__Len`: GIS-computed line length.

## `spend_by_home_dallas_county_2024`

CSV file: `data/spend_by_home_dallas_county_2024/trends-spend-home-v2_from-month-of-2024-01-01-to-month-of-2024-12-31--full-week_dct.csv`

This Replica spending table estimates 2024 monthly consumer spending by home tract of the residents who spent money. It includes total population and spending by merchant category, with online/offline splits for grocery, restaurants/bars, and retail.

- `month_starting`: First day of the month represented by the row.
- `geo_id`: Census geography identifier.
- `geo_name`: Geography name.
- `population`: Population of the geography.
- `airline_hospitality_car_rental_spend_total`: Total spend in airline, hospitality, and car-rental category.
- `entertainment_recreation_spend_total`: Total entertainment and recreation spend.
- `gas_stations_parking_taxis_tolls_spend_total`: Total spend at gas stations, parking, taxis, and tolls.
- `grocery_stores_spend_offline`: In-person grocery spend.
- `grocery_stores_spend_online`: Online grocery spend.
- `restaurants_bars_spend_offline`: In-person restaurants and bars spend.
- `restaurants_bars_spend_online`: Online restaurants and bars spend.
- `retail_spend_offline`: In-person retail spend.
- `retail_spend_online`: Online retail spend.

## `spend_by_merchant_dallas_county_2024`

CSV file: `data/spend_by_merchant_dallas_county_2024/trends-spend-merchant-v2_from-month-of-2024-01-01-to-month-of-2024-12-31--full-week_dct.csv`

This Replica spending table estimates 2024 monthly in-person consumer spending by merchant tract. It shows where spending occurred, not where the spender lives.

- `month_starting`: First day of the month represented by the row.
- `geo_id`: Census geography identifier.
- `geo_name`: Geography name.
- `population`: Population of the geography.
- `airline_hospitality_car_rental_spend`: Spend in airline, hospitality, and car-rental category.
- `entertainment_recreation_spend`: Entertainment and recreation spend.
- `gas_stations_parking_taxis_tolls_spend`: Spend at gas stations, parking, taxis, and tolls.
- `grocery_stores_spend`: Grocery store spend.
- `restaurants_bars_spend`: Restaurants and bars spend.
- `retail_spend`: Retail spend.

## `street_maintenance_completed_city_of_dallas`

CSV file: `data/street_maintenance_completed_city_of_dallas/csv/street_maintenance_completed_city_of_dallas.csv`

This line layer describes completed street maintenance projects in Dallas, including project identifiers, work type, street limits, dates, cost, length, contractor, funding source, and district fields.

- `WKT`: Maintenance project line geometry.
- `OBJECTID`: Source GIS record identifier.
- `SRD_PRJ_ID`, `PSI_PRJ_ID`: Project identifiers.
- `SRD_PRJ_FY`: Project fiscal year.
- `ACTN_ID`, `ACTN_NAME`, `ACTN_CLASS`: Maintenance action identifier/name/class.
- `ST_ID`, `ST_PREFIX`, `ST_NAME`, `ST_TYPE`, `ST_SUFFIX`, `ST_FULLNAM`: Street identifiers and name components.
- `FROM_BLOCK`, `TO_BLOCK`: Project limits.
- `PRJ_DESC`: Project description.
- `MNGR_NAME`: Project manager.
- `STATUS`: Project status.
- `EST_START`, `ACT_START`, `ACT_STOP`: Estimated and actual dates.
- `PRJ_COST`: Project cost.
- `LENGTH_FT`, `LNMILES`: Project length in feet/lane-miles.
- `CD11_NUM`: Council district or district number field.
- `LAST_UPDAT`: Last update date.
- `CONTRACTOR`: Contractor.
- `FUNDING_SO`: Funding source.
- `IN_EQUITY`: Equity-area indicator.
- `MAINT_DIST`: Maintenance district.
- `EAST_WEST`: East/west classification.
- `Shape__Len`: GIS-computed line length.

## `street_with_traffic_calming_city_of_dallas`

CSV file: `data/street_with_traffic_calming_city_of_dallas/csv/street_with_traffic_calming.csv`

This line layer identifies streets with traffic calming treatments in Dallas.

- `WKT`: Street segment geometry.
- `OBJECTID`: Source GIS record identifier.
- `STID`: Street identifier.
- `STREET`, `FROM_STREE`, `TO_STREET`: Street name and segment limits.
- `COUNCIL_DI`: Council district.
- `DATE_INSTA`: Installation date.
- `INSTALLER`: Installer.
- `FY`: Fiscal year.
- `MAPSCO`: Map grid reference.
- `DEVICETYPE`: Traffic calming device type.
- `COMMENT`: Source comments.
- `PR_STATUS`: Project/status field.
- `EQUITY_SCO`: Equity score.
- `NUMBER_DEV`: Number of devices.
- `FYQuarter`: Fiscal quarter.
- `MapField`: Mapping field.
- `created_us`, `created_da`, `last_edite`, `last_edi_1`, `CreationDa`, `Creator`, `EditDate`, `Editor`: Source edit audit fields.
- `Shape__Len`: GIS-computed line length.

## `striped_street_city_of_dallas`

CSV file: `data/striped_street_city_of_dallas/csv/striped_street.csv`

This line layer describes striped streets in Dallas, including striping configuration, dates, mileage, council districts, project fields, and pavement percentages.

- `WKT`: Striped-street segment geometry.
- `OBJECTID`: Source GIS record identifier.
- `SD_ID`: Striping/segment identifier.
- `StreetName`, `StartStree`, `Finish_Str`: Street name and segment endpoints.
- `Mapsco`: Map grid reference.
- `Configurat`: Striping configuration.
- `LastStripi`, `LastStri_1`, `ButtonsDat`: Last striping/button dates or related fields.
- `LinearMile`, `RoadMilesG`: Linear miles and road-mile fields.
- `CouncilD`, `NumberCoun`, `CD1`, `CD2`, `CD3`, `CD4`, `CD5`: Council district fields.
- `Comment`: Source comments.
- `Descriptio`: Description.
- `PlanYear`: Plan year.
- `CBD`: Central business district indicator.
- `PrepSeal`: Prep/seal field.
- `AsphaltPer`, `ConcretePe`: Asphalt/concrete percentage fields.
- `SpeedLimit`: Posted speed limit.
- `CLASSIF`: Road classification.
- `PIZ`, `PIZName`: Program/investment zone fields.
- `ACT_COMPLE`: Actual completion date.
- `PercentonH`, `LMonHIN`: High-injury-network related fields.
- `Sched_Date`: Scheduled date.
- `PR_TYPE`, `PR_STATUS`: Project type and status.
- `PM_NAME`, `PM_EMAIL`, `PM_PHONE`: Project manager contact fields.
- `DEPARTMENT`: Responsible department.
- `created_us`, `created_da`, `last_edite`, `last_edi_1`: Source edit audit fields.
- `Shape__Len`: GIS-computed line length.

## `tc_permit_details_city_of_dallas`

CSV files:

- `data/tc_permit_details_city_of_dallas/line/traffic_control_permit.csv`
- `data/tc_permit_details_city_of_dallas/point/traffic_control_permit_point.csv`

These City of Dallas datasets describe traffic-control permits as line and point records. They include permit identifiers, permit type, status, dates, work description, applicant/contractor names, lane closures, case IDs, and locations.

Shared permit columns:

- `OBJECTID`: Source GIS record identifier.
- `JOBID`: Job identifier.
- `EXTERNALFILENUM`: External permit/file number.
- `PERMITTYPE`: Permit type.
- `COMMERCIALORRESIDENTIAL`: Commercial/residential classification.
- `STATUSDESCRIPTION`: Permit status.
- `CREATEDDATE`, `ISSUEDATE`, `COMPLETEDDATE`, `EXPIRATIONDATE`: Permit lifecycle dates.
- `ROWREQUESTEDSTARTDATE`, `ROWESTIMATEDCOMPLETIONDATE`: Right-of-way work dates.
- `ROWISEMERGENCYREPAIR`: Emergency repair indicator.
- `SPECIFICLOCATION`: Location description.
- `WORKDESCRIPTION`: Description of permitted work.
- `APPLICANTNAMESTORED`, `APPLICANTCOMPANYNAMESTORED`: Applicant fields.
- `ALLCONTRACTORSNAME`: Contractor names.
- `LEGEND`: Legend/classification field.
- `TCREASONFORJOB`: Traffic-control reason.
- `ROWNUMBEROFLANESCLOSED`: Number of lanes closed.
- `CASEID`: Case identifier.
- `LOCATIONNAMES`: Location names.

Line-only column:

- `Shape__Length`: GIS-computed line length.

Point-only columns:

- `X`, `Y`: Permit point coordinates.
- `COUNCIL_DISTRICTS`, `INSPECTION_DISTRICTS`: District fields.

## `traffic_calming_device_city_of_dallas`

CSV file: `data/traffic_calming_device_city_of_dallas/csv/traffic_calming_device.csv`

This point layer describes individual traffic calming devices in Dallas.

- `X`, `Y`: Device point coordinates.
- `OBJECTID`: Source GIS record identifier.
- `LOCID`: Location identifier.
- `STID`: Street identifier.
- `STREET`, `FROM_STREE`, `TO_STREET`: Street and segment limits.
- `COUNCIL_DI`: Council district.
- `DATE_INSTA`: Installation date.
- `INSTALLER`: Installer.
- `FY`: Fiscal year.
- `MAPSCO`: Map grid reference.
- `DEVTYPE`: Device type.
- `NUM_CUSHIO`: Number of cushions or related count.
- `DecadeInst`: Installation decade.
- `EQUITY_SCO`: Equity score.
- `created_us`, `created_da`, `last_edite`, `last_edi_1`, `CreationDa`, `Creator`, `EditDate`, `Editor`: Source edit audit fields.

## `traffic_signs_city_of_dallas`

CSV file: `data/traffic_signs_city_of_dallas/csv/traffic_sign.csv`

This point layer inventories traffic signs in Dallas.

- `X`, `Y`: Sign point coordinates.
- `OBJECTID`: Source GIS record identifier.
- `SIGNID`, `NewSignID`, `GlobalID`: Sign identifiers.
- `CORNER`, `SideofRoad`: Sign location relative to intersection/roadway.
- `SOS`, `DSF`: Source operational fields.
- `CODE`: Sign code.
- `MAIN_ST`, `CROSS_ST`, `ADDRESS`: Location fields.
- `InstDate`: Installation date.
- `MaintDist`: Maintenance district.
- `PriorityZo`: Priority zone.
- `CouncilDis`: Council district.
- `Schedule`: Schedule field.
- `Mapsco`: Map grid reference.
- `ReplDate`: Replacement date.
- `CrewLeader`: Crew leader.
- `JobSource`: Work source.
- `RefNumber`: Reference number.
- `JobAction`: Job action.
- `SignAge`: Sign age.
- `SIGN_TEXT`: Text printed on the sign.
- `SignSuppor`: Sign support type.
- `SignName`: Sign name.
- `SignSymbol`: Sign symbol.

## `trails_dallas_county`

CSV file: `data/trails_dallas_county/csv/trails.csv`

This line layer describes existing off-street trails in Dallas County.

- `WKT`: Trail line geometry.
- `OBJECTID`: Source GIS record identifier.
- `Status`: Facility status.
- `OnOffStr`: On-street/off-street classification.
- `FuncClass`: Functional class.
- `RegCorr`: Regional corridor field.
- `FacType`: Facility type, such as shared-use path.
- `AlignPend`: Alignment-pending field.
- `Shape.STLength()`: GIS-computed line length.
- `StateNetCat`: State network category.
- `Name`: Trail name.
- `Source`: Source of the feature.

## `turning_movement_count_dallas_county_2022`

CSV file: `data/turning_movement_count_dallas_county_2022/tmc_fall-2022_dct.csv`

This Replica table contains 2022 turning movement counts for Dallas County intersections, with hourly counts by day of week and movement direction.

- `intersection_id`: Unique intersection identifier.
- `intersection_id_geom`: Intersection point geometry in WKT.
- `turn_maneuver`: Maneuver type, such as left, right, through, or U-turn.
- `movement_direction`: Start-to-end compass movement, such as `E_to_N`.
- `inbound_direction`: Inbound compass direction.
- `inbound_heading`: Inbound heading in degrees from north.
- `turning_movement`: Standard movement code, such as `EBL` or `NBT`.
- `state`: State abbreviation.
- `inbound_stable_edge_id`: Replica inbound road-link identifier.
- `inbound_street_name`: Inbound street name.
- `outbound_osm_id`: Outbound OpenStreetMap way or supersegment identifier.
- `outbound_street_name`: Outbound street name.
- `hour`: Hour of day in local 24-hour time.
- `day`: Day of week.
- `count`: Estimated/scaled turning movement count.

## Open Questions

- Should the crash datasets be cleaned before student use to remove fields such as `VIN`, driver ZIP codes, and owner ZIP codes?
- Should the Census ACS tables be converted from wide coded format into long, student-friendly tables with one row per tract/measure?
- Do you want CSV exports created for the folders that currently only have shapefiles or GeoPackages?
