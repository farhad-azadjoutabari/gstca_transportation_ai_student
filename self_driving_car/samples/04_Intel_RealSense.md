# Intel RealSense D435 Camera

The QCar2 is equipped with an Intel RealSense D435 depth camera that provides both an RGB image and a depth image. Unlike the CSI cameras, the RealSense can estimate the distance from the camera to objects in the scene, making it useful for obstacle detection, object localization, autonomous navigation, and perception.

The Quanser Python library provides a wrapper that automatically aligns the RGB and depth images, allowing every RGB pixel to correspond to the correct depth measurement.

This example also demonstrates how to use the built-in YOLOv8 segmentation model together with the aligned depth image to detect objects and estimate their distance from the vehicle.

---

# Required Libraries

```python
import numpy as np
import cv2
import time

from pit.YOLO.nets import YOLOv8
from pit.YOLO.utils import QCar2DepthAligned
```

---

# Initializing the RealSense Camera

Create the aligned RGB/depth camera object.

```python
QCarImg = QCar2DepthAligned()
```

This object automatically initializes the Intel RealSense camera and aligns the RGB and depth streams.

No additional camera configuration is required.

---

# Reading Images

Read one synchronized frame from the camera.

```python
QCarImg.read()
```

After calling `read()`, two images become available:

```python
QCarImg.rgb
QCarImg.depth
```

Both images correspond to exactly the same scene.

---

# RGB Image

The RGB image is a standard OpenCV image.

```python
rgb = QCarImg.rgb
```

Image properties:

| Property | Value |
|----------|-------|
| Type | `numpy.ndarray` |
| Color Format | **RGB** |
| Channels | 3 |
| Resolution | 640 × 480 |
| Data Type | `uint8` |

Example:

```python
print(QCarImg.rgb.shape)
```

Output

```text
(480, 640, 3)
```

The image can be used directly with OpenCV.

```python
gray = cv2.cvtColor(QCarImg.rgb, cv2.COLOR_BGR2GRAY)

edges = cv2.Canny(gray,50,150)
```

---

# Depth Image

The depth image stores the measured distance from the camera for every pixel.

```python
depth = QCarImg.depth
```

Unlike the RGB image, the depth image is **not** a color image.

Each pixel contains a depth value.

Example:

```python
print(QCarImg.depth.shape)
```

Output

```text
(480,640)
```

Since the RGB and depth images are aligned, a pixel at

```text
(x,y)
```

represents the same physical point in both images.

This alignment allows computer vision algorithms to detect an object in the RGB image and immediately retrieve its distance from the depth image.

---

# Using YOLOv8

Create the segmentation model.

```python
myYolo = YOLOv8(
    imageWidth=640,
    imageHeight=480
)
```

The model performs object detection and instance segmentation.

---

# Pre-processing

Prepare the RGB image for inference.

```python
rgbProcessed = myYolo.pre_process(
    QCarImg.rgb
)
```

The preprocessing step performs the required image resizing and formatting expected by the neural network.

---

# Running Inference

Run the segmentation model.

```python
prediction = myYolo.predict(

    inputImg=rgbProcessed,

    classes=[2,9,11],

    confidence=0.3,

    half=True,

    verbose=False
)
```

### Parameters

| Parameter | Description |
|-----------|-------------|
| `classes` | Object classes to detect |
| `confidence` | Minimum confidence threshold |
| `half=True` | Uses FP16 inference for faster execution |
| `verbose=False` | Disable console output |

---

# COCO Class IDs

The example detects only three object categories.

| ID | Object |
|----|--------|
| 2 | Car |
| 9 | Traffic Light |
| 11 | Stop Sign |

Any valid COCO class ID may be used.

Example:

```python
classes=[0]
```

detects only people.

---

# Combining Detection with Depth

After inference, combine the segmentation results with the aligned depth image.

```python
processedResults = myYolo.post_processing(

    alignedDepth=QCarImg.depth,

    clippingDistance=5
)
```

This function calculates the distance from the camera to every detected object.

The parameter

```python
clippingDistance=5
```

limits the maximum valid depth measurement to **5 meters**.

Objects farther than this distance are ignored.

---

# Accessing Detection Results

Each detected object is returned as an object containing its information.

```python
for obj in processedResults:

    print(obj.__dict__)
```

Typical information includes

- detected class
- confidence
- segmentation mask
- bounding box
- estimated distance
- image location

The exact fields depend on the Quanser implementation.

---

# Rendering Results

Generate an annotated image.

```python
annotatedImg = myYolo.post_process_render(
    showFPS=True
)
```

The rendered image typically contains

- segmentation masks
- bounding boxes
- object labels
- confidence scores
- estimated distances
- FPS information

Display the result using OpenCV.

```python
cv2.imshow(
    "Object Segmentation",
    annotatedImg
)
```

---

# Typical Processing Pipeline

The complete perception pipeline is

```text
Intel RealSense
        │
        ▼
Acquire RGB + Depth
        │
        ▼
Align RGB and Depth
        │
        ▼
YOLOv8 Pre-processing
        │
        ▼
YOLOv8 Segmentation
        │
        ▼
Combine with Depth Image
        │
        ▼
Estimate Distance
        │
        ▼
Render Detection Results
```

---

# Minimal Example

```python
QCarImg.read()

rgbProcessed = myYolo.pre_process(
    QCarImg.rgb
)

myYolo.predict(
    inputImg=rgbProcessed,
    classes=[2,9,11]
)

results = myYolo.post_processing(
    alignedDepth=QCarImg.depth,
    clippingDistance=5
)

for obj in results:
    print(obj.__dict__)
```

---

# Terminating the Camera

Always terminate the camera before exiting the program.

```python
QCarImg.terminate()
```

This properly closes the Intel RealSense device and releases all associated resources.
