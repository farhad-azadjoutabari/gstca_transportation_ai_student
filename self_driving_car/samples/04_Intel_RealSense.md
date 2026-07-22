# Chapter 4 – Intel RealSense

## Overview

The Intel RealSense provides synchronized RGB and depth images. It allows the vehicle to estimate the distance to detected objects.

## Data Streams

- RGB image
- Depth image

## Processing Pipeline

```
RGB Image
   │
Object Detection
   │
Depth Image
   │
Distance Calculation
   │
Vehicle Decision
```

## Example Workflow

```python
read_rgb()
read_depth()
detect_object()
measure_distance()
```

## Typical Applications

- Stop-sign detection
- Obstacle detection
- Distance-based stopping

## Tips

Always use aligned depth images so that depth pixels correspond to RGB pixels.
