# Chapter 1 – Introduction to QCar2 Python Programming

## Welcome

The Quanser QCar2 is an educational autonomous vehicle platform designed for learning robotics, computer vision, AI, and control systems. This guide focuses on developing Python applications that interact with the vehicle's sensors and actuators.

Unlike a normal Python application, a QCar program continuously communicates with hardware. Every program follows the same basic cycle:

1. Initialize hardware.
2. Read sensor data.
3. Process information.
4. Make a decision.
5. Send control commands.
6. Repeat until the program exits.

## Overall Architecture

```
Sensors
   │
   ▼
Python Program
   │
Decision Logic
   │
   ▼
Vehicle Commands
```

## Main Hardware Modules

- QCar vehicle controller
- CSI cameras
- Intel RealSense RGB/Depth camera
- RPLidar
- Probe/Observer visualization

## Typical Program Structure

```python
initialize_devices()

try:
    while True:
        read_sensors()
        process_data()
        control_vehicle()
finally:
    terminate_devices()
```

## Good Programming Practices

- Keep sensor reading separate from decision making.
- Always terminate hardware objects.
- Start with one sensor before combining multiple modules.
- Test individual modules independently before integration.

## Next Step

The next chapter explains how to send steering and throttle commands to the QCar.
