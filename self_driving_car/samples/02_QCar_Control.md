# Chapter 2 – Vehicle Control

## Purpose

The QCar library provides access to steering, throttle and LEDs. Almost every application begins by creating a QCar object.

## Import

```python
from pal.products.qcar import QCar
```

## Creating the Vehicle

```python
qcar = QCar()
```

## Sending Commands

```python
throttle = 0.08
steering = 0.0
leds = [0]*8

qcar.write(throttle, steering, leds)
```

## Typical Control Loop

```python
while running:
    throttle = compute_speed()
    steering = compute_steering()
    qcar.write(throttle, steering, leds)
```

## API Reference

| Method | Description |
|---|---|
|QCar()|Initialize the vehicle|
|write(throttle, steering, leds)|Send commands|
|terminate()|Release hardware resources|

## Example – Drive Forward

```python
qcar = QCar()

try:
    while True:
        qcar.write(0.08, 0.0, [0]*8)
finally:
    qcar.terminate()
```

## Tips

- Use small throttle values while testing.
- Never exit without calling `terminate()`.
