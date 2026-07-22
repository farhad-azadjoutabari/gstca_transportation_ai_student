# Chapter 5 – RPLidar

## Overview

The RPLidar measures distances in a full 360° scan around the vehicle.

Each scan returns two important arrays:

- angles
- distances

## Processing Pipeline

```
LiDAR
   │
Read Scan
   │
Angles + Distances
   │
Obstacle Detection
   │
Stop Vehicle
```

## Example Logic

```python
lidar.read()

minimum_distance = min(distances)

if minimum_distance < 0.5:
    stop_vehicle()
```

## Common Applications

- Collision avoidance
- Safety stop
- Mapping
- Navigation

## Tips

Filter invalid measurements before making decisions.
