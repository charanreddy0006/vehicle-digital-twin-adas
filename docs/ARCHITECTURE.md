# Architecture

AutoTwin is organized into independent domain layers.

## Core

Defines enums and domain models. No dashboard dependencies.

## Vehicle

Contains the digital twin and reusable physical components:

- Battery
- Brake system
- Tire system
- Vehicle dynamics

## Environment

Models the road and moving objects.

## Sensors

All sensors implement the abstract `Sensor` interface. Concrete sensors are interchangeable.

## Perception

`SensorFusion` combines observations from multiple sensors into fused objects.

## ADAS

All ADAS modules implement the abstract `ADASModule` interface.

```text
ADASModule
├── FCW
├── AEB
├── ACC
├── LDW
└── BSD
```

## Simulation

The simulation engine coordinates:

```text
Sensors
   ↓
Fusion
   ↓
ADAS
   ↓
Vehicle Control
   ↓
Vehicle Dynamics
   ↓
World Update
   ↓
Telemetry
```

## Presentation

The CLI runs simulations and the Streamlit dashboard visualizes completed runs.

This separation allows future integration with computer vision, ML, CARLA, or ROS 2 without replacing the domain model.
