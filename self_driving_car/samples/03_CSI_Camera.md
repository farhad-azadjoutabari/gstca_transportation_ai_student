# CSI Cameras

The QCar2 provides four onboard CSI cameras that can be accessed directly from Python using the `QCarCameras` class. These cameras provide synchronized image streams that can be used for computer vision, lane following, object detection, SLAM, and many other autonomous driving applications.

The camera images are stored as **OpenCV BGR images**, meaning they can be used directly with OpenCV functions without any conversion.

---

# Required Libraries

```python
import time
import cv2

from pal.products.qcar import QCarCameras
from pal.utilities.probe import Probe
```

---

# Creating the Camera Object

Create a `QCarCameras` object and enable only the cameras you need.

```python
cameras = QCarCameras(
    enableFront=True,
    enableBack=True,
    enableLeft=True,
    enableRight=True,
)
```

Each parameter is a Boolean.

| Parameter | Description |
|-----------|-------------|
| `enableFront` | Enable the front CSI camera |
| `enableBack` | Enable the rear CSI camera |
| `enableLeft` | Enable the left CSI camera |
| `enableRight` | Enable the right CSI camera |

For example, if only the front camera is needed:

```python
cameras = QCarCameras(
    enableFront=True
)
```

Enabling only the required cameras reduces CPU usage.

---

# Reading Images

Capture one frame from every enabled camera:

```python
flags = cameras.readAll()
```

`readAll()` performs two tasks:

1. Reads one new image from every enabled camera.
2. Updates the internal image buffers.

It returns a list of Boolean values indicating whether each camera successfully captured an image.

Example:

```python
flags = [True, True, True, True]
```

A common practice is to verify that all cameras succeeded before using the images:

```python
if all(flags):
    print("All cameras captured successfully.")
```

---

# Accessing Individual Cameras

The enabled cameras are stored inside

```python
cameras.csi
```

Each element is a camera object.

Example:

```python
front = cameras.csi[0]
back  = cameras.csi[1]
left  = cameras.csi[2]
right = cameras.csi[3]
```

If only one camera is enabled, it will appear as

```python
cameras.csi[0]
```

regardless of which camera was enabled.

---

# Accessing the Image

Each camera object contains

```python
camera.imageData
```

For example:

```python
front_image = cameras.csi[0].imageData
```

The returned image is a standard OpenCV image.

---

# Image Format

The image returned by the CSI camera has the following format:

- Data type: `numpy.ndarray`
- Color order: **BGR**
- Channels: 3
- Resolution: **820 × 410**
- Data type: `uint8`

Example:

```python
print(front_image.shape)
```

Output:

```text
(410, 820, 3)
```

where

- 410 = image height
- 820 = image width
- 3 = Blue, Green, Red channels

Since the image is already in **BGR** format, it can be used directly with OpenCV.

Example:

```python
gray = cv2.cvtColor(front_image, cv2.COLOR_BGR2GRAY)

hsv = cv2.cvtColor(front_image, cv2.COLOR_BGR2HSV)

edges = cv2.Canny(gray, 50, 150)
```

No RGB-to-BGR conversion is required.

---

# Processing Every Camera

The cameras can be processed individually:

```python
flags = cameras.readAll()

if all(flags):

    front = cameras.csi[0].imageData
    back  = cameras.csi[1].imageData
    left  = cameras.csi[2].imageData
    right = cameras.csi[3].imageData
```

or by looping through all cameras:

```python
for i, camera in enumerate(cameras.csi):

    image = camera.imageData

    # Process image here
```

---

# Streaming Images to the Observer

The Quanser Observer can display images remotely on the host PC.

First create a `Probe` object using the IP address of the computer running `observer.py`.

```python
probe = Probe(ip="192.168.3.10")
```

Create one display window for each camera:

```python
for i in range(4):

    probe.add_display(
        imageSize=[410, 820, 3],
        scaling=True,
        scalingFactor=2,
        name="CSI" + str(i)
    )
```

---

# Sending Images

After capturing a frame,

```python
flags = cameras.readAll()
```

send the image to the Observer:

```python
for i, camera in enumerate(cameras.csi):

    probe.send(
        name="CSI" + str(i),
        imageData=camera.imageData
    )
```

Each display window receives the image whose name matches the display name.

---

# Complete Example

```python
from pal.products.qcar import QCarCameras
from pal.utilities.probe import Probe

cameras = QCarCameras(
    enableFront=True,
    enableBack=True,
    enableLeft=True,
    enableRight=True
)

probe = Probe(ip="192.168.3.10")

for i in range(4):

    probe.add_display(
        imageSize=[410, 820, 3],
        scaling=True,
        scalingFactor=2,
        name="CSI" + str(i)
    )

while True:

    if not probe.connected:
        probe.check_connection()

    if probe.connected:

        flags = cameras.readAll()

        if all(flags):

            for i, camera in enumerate(cameras.csi):

                probe.send(
                    name="CSI" + str(i),
                    imageData=camera.imageData
                )
```

---

# Terminating the Cameras

Always terminate the cameras before exiting the program.

```python
cameras.terminate()
probe.terminate()
```

This properly releases the camera resources and closes the communication with the Observer.
