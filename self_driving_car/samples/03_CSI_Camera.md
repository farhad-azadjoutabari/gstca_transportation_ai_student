# Chapter 3 – CSI Camera

## Overview

The CSI cameras provide high-speed video for lane following and computer vision algorithms.

## Required Library

```python
from pal.utilities.vision import Camera2D
```

## Opening the Camera

```python
camera = Camera2D(...)
```

## Reading an Image

```python
camera.read()
frame = camera.image_data
```

The `image_data` property contains the latest RGB image and can be processed using OpenCV.

## Visualization (Important)

Because the CSI camera uses the Jetson platform, viewing the stream through Remote Desktop is unreliable.

Recommended workflow:

1. Start **XLaunch** on your local PC.
2. Open the **Observer** application.
3. Connect to the QCar using **PuTTY**.
4. Run the **Probe**.
5. Execute your Python program.

```
CSI Camera
    │
 Probe (QCar)
    │
 Network
    │
 Observer (PC)
    │
 XLaunch Display
```

## Example

```python
while True:
    camera.read()
    frame = camera.image_data
    # Process frame here
```

## Applications

- Lane following
- Color segmentation
- Object tracking
