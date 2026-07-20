# CRS and Distance Guide

This guide explains the coordinate reference system, or CRS, idea used in this
project. It is written for project work, not for GIS theory. The goal is to
help you measure distance, length, and buffers correctly in the Dallas-area
transportation datasets.

## The Simple Idea

A CRS tells Python how the coordinates in a map layer should be understood.

For example, a point can be stored as two numbers:

```text
-96.80, 32.78
```

Those numbers only make sense if we know the CRS. In this case they are likely
longitude and latitude, which means the point is near Dallas.

When we do spatial work, CRS affects questions like:

- How far is one point from another?
- How long is this road segment?
- What is within 150 feet of this intersection?
- How many crashes are within 100 feet of a road?

## Two Common CRS Types

### 1. Geographic CRS

A geographic CRS stores locations using longitude and latitude.

The most common one is:

```python
EPSG:4326
```

This is often called WGS84. It is great for storing locations and sharing data
online. Many CSV files with `Latitude` and `Longitude` columns are in
`EPSG:4326`.

But longitude and latitude are measured in degrees, not feet or meters. That
means they are not good for measuring distance directly.

This is a problem:

```python
gdf.geometry.length
gdf.geometry.distance(other.geometry)
gdf.geometry.buffer(150)
```

If `gdf` is still in `EPSG:4326`, those calculations are happening in degrees.
A buffer of `150` would mean 150 degrees, not 150 feet.

### 2. Projected CRS

A projected CRS stores locations on a flat coordinate system. For a local area,
this makes distance and length calculations much more meaningful.

For this project, the notebooks use:

```python
PROJECTED_EPSG = 2276
```

`EPSG:2276` is a projected CRS for North Central Texas. It is appropriate for
Dallas-area work. Its coordinate units are US survey feet. For this class
project, you can think of its distance values as feet.

That means:

```python
distance=150
```

means about 150 feet when the calculation is being done in `EPSG:2276`.

## The Project Rule

Use longitude/latitude for storing and mapping locations.

Use `EPSG:2276` for Dallas-area measurements:

- buffers
- nearest distance
- road length
- polygon area
- crash counts within a distance
- signs, crosswalks, or signals within a distance

In the instructor notebooks you will often see:

```python
PROJECTED_EPSG = 2276
```

That is the project CRS for distance-based calculations.

## Useful Distance Values

Because `EPSG:2276` uses feet, these values are useful:

| Distance | Feet |
| --- | ---: |
| 100 feet | 100 |
| 150 feet | 150 |
| 250 feet | 250 |
| 500 feet | 500 |
| Quarter mile | 1320 |
| Half mile | 2640 |
| One mile | 5280 |
| Three miles | 15840 |

Example:

```python
intersections = summarize_points_within_distance(
    intersections,
    traffic_signs,
    distance=150,
    count_column="traffic_signs_within_150ft",
    projected_epsg=2276,
)
```

This counts signs within 150 feet of each intersection.

## How to Check a CRS

After reading a spatial file, check its CRS:

```python
gdf.crs
```

Or use the helper:

```python
from helper.spatial import check_crs

check_crs(gdf)
```

If the CRS says `EPSG:4326`, the coordinates are probably longitude and
latitude. Good for location, not good for distance.

If the CRS says `EPSG:2276`, it is ready for Dallas-area distance calculations.

## How to Convert CRS

There are two different operations that students often mix up.

### Set CRS

Use `set_crs` only when the data has no CRS label but you know what CRS the
coordinates already use.

Example: a CSV has longitude and latitude columns, so you create points and
assign `EPSG:4326`.

```python
import geopandas as gpd

crashes = gpd.GeoDataFrame(
    crash_table,
    geometry=gpd.points_from_xy(crash_table["Longitude"], crash_table["Latitude"]),
    crs="EPSG:4326",
)
```

This does not move the points. It labels the coordinate system.

### Transform CRS

Use `to_crs` when the data already has a CRS and you want to convert the
coordinates to another CRS.

```python
crashes_2276 = crashes.to_crs(epsg=2276)
```

This changes the coordinate values so that measurements can be made in the new
CRS.

## Recommended Helper Workflow

The easiest project workflow is to use `prepare_spatial_data`.

```python
from helper.spatial import prepare_spatial_data

roads = prepare_spatial_data(
    roads,
    projected_epsg=2276,
    warn_if_geographic=False,
)
```

This helper:

- checks that the data is spatial
- removes missing or empty geometries
- projects the layer to `EPSG:2276`
- prepares the layer for distance, length, and buffer work

If a layer has no CRS but you know it is longitude/latitude, use:

```python
points = prepare_spatial_data(
    points,
    input_crs=4326,
    projected_epsg=2276,
    warn_if_geographic=False,
)
```

## Helper Functions and Units

Different helpers handle units slightly differently. These are the most common
patterns.

### Buffer or nearby summaries

For helpers like:

```python
summarize_points_within_distance(...)
summarize_lines_within_distance(...)
summarize_polygons_within_distance(...)
```

the `distance` value is in the units of the projected CRS. In this project,
with `projected_epsg=2276`, that means feet.

```python
roads = summarize_points_within_distance(
    roads,
    crashes,
    distance=100,
    count_column="crashes_within_100ft",
    projected_epsg=2276,
)
```

### Length

For road length, use:

```python
from helper.spatial import calculate_length

roads = calculate_length(
    roads,
    column_name="road_length_miles",
    unit="miles",
    projected_epsg=2276,
)
```

The helper does the projection and returns the length in miles.

### Nearest distance

For nearest features, use:

```python
from helper.spatial import add_nearest_distance

intersections = add_nearest_distance(
    intersections,
    tmc_points,
    distance_column="distance_to_tmc_ft",
    unit="feet",
    projected_epsg=2276,
)
```

Or, when attaching several nearest layers:

```python
from helper.spatial import attach_nearest_features

intersections = attach_nearest_features(
    intersections,
    {
        "signal": signals,
        "major_road": major_roads,
    },
    unit="feet",
    projected_epsg=2276,
)
```

These helpers return distances in the `unit` you request.

## Common Mistakes

### Mistake 1: Measuring in longitude/latitude

If your CRS is `EPSG:4326`, do not measure distance directly.

Avoid:

```python
roads["length"] = roads.geometry.length
```

unless the roads have already been projected.

Better:

```python
roads = calculate_length(
    roads,
    column_name="road_length_miles",
    unit="miles",
    projected_epsg=2276,
)
```

### Mistake 2: Using `set_crs` when you should use `to_crs`

Use `set_crs` only to label coordinates that have no CRS.

Use `to_crs` to convert coordinates from one CRS to another.

Wrong:

```python
gdf = gdf.set_crs(epsg=2276)
```

if the coordinates are actually longitude and latitude.

Better:

```python
gdf = gdf.set_crs(epsg=4326)
gdf = gdf.to_crs(epsg=2276)
```

or:

```python
gdf = prepare_spatial_data(gdf, input_crs=4326, projected_epsg=2276)
```

### Mistake 3: Forgetting what the distance number means

In project helper calls with `projected_epsg=2276`:

```python
distance=150
```

means 150 feet.

It does not mean 150 meters or 150 miles.

## Challenge Examples

### Challenge 3

Count speed-related crashes within 100 feet of each road segment:

```python
roads = summarize_crashes_by_road(
    crash_gdf,
    roads,
    buffer_distance=100,
    count_column="speed_related_crash_count",
    road_id_column="OBJECTID",
    projected_epsg=2276,
)
```

### Challenge 4

Count intersection-related crashes within 150 feet of each signalized
intersection:

```python
intersections = summarize_crashes_by_intersection(
    crash_gdf,
    intersections,
    buffer_distance=150,
    count_column="intersection_crash_count",
    intersection_id_column="OBJECTID",
    projected_epsg=2276,
)
```

Attach the nearest turning-movement-count point within 300 feet:

```python
intersections = attach_nearest_features(
    intersections,
    [
        {
            "name": "tmc",
            "gdf": tmc_gdf,
            "distance_column": "distance_to_tmc_ft",
            "columns": ["tmc_total_volume"],
            "max_distance": 300,
            "unit": "feet",
        }
    ],
    projected_epsg=2276,
)
```

## Quick Checklist

Before doing distance work, ask:

1. Does my layer have a CRS?
2. Is it longitude/latitude, such as `EPSG:4326`?
3. Did I project to `EPSG:2276` for Dallas-area distance work?
4. Am I clear whether my distance is feet, miles, or meters?
5. Am I using helper functions that handle CRS and units for me?

When in doubt, use:

```python
gdf.crs
```

and then prepare the layer:

```python
gdf = prepare_spatial_data(gdf, projected_epsg=2276)
```

