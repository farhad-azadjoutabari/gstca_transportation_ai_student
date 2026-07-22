# Chapter 6 – Observer and Probe

## Purpose

Observer provides a convenient way to visualize data generated on the QCar without relying on Remote Desktop.

## Architecture

```
Python Program
      │
   Probe
      │
 Ethernet
      │
  Observer
      │
 Local Display
```

## Typical Startup Procedure

### Local PC

1. Start XLaunch.
2. Launch Observer.

### QCar

1. Connect using PuTTY.
2. Start Probe.
3. Run your Python application.

## What Can Be Displayed?

- CSI camera images
- Lane detection overlays
- RGB images
- LiDAR scans
- Custom OpenCV windows

## Best Practices

- Use a single Observer window when possible.
- Close Observer after terminating the Python program.
- Always terminate hardware resources before exiting.
