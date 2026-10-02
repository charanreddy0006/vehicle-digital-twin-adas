# AutoTwin ADAS

## Vehicle Digital Twin and Advanced Driver Assistance System Simulation Platform

AutoTwin ADAS is a modular Python-based simulation platform for modeling a virtual vehicle, automotive sensors, sensor fusion, and Advanced Driver Assistance Systems (ADAS).

The project demonstrates how automotive software components can be designed using object-oriented programming, scenario-based simulation, perception pipelines, safety logic, telemetry, and an engineering-oriented visualization dashboard.

> **Educational and research project.** AutoTwin ADAS is a simplified software simulation and is not safety-certified automotive software. It must not be connected to or used to control a real vehicle.

---

## Overview

Modern vehicles combine multiple sensors and software systems to understand their surroundings and assist the driver.

AutoTwin ADAS recreates a simplified version of this software architecture:

```text
Scenario / Road Environment
            |
            v
     Vehicle Digital Twin
            |
            v
       Sensor Suite
            |
    +-------+--------+----------------+
    |       |        |                |
  Radar  Camera  Ultrasonic      IMU / GPS
    |       |        |                |
    +-------+--------+----------------+
            |
            v
       Sensor Fusion
            |
            v
       ADAS Decision Layer
            |
    +-------+--------+--------+--------+
    |       |        |        |        |
   FCW     AEB      ACC      LDW      BSD
            |
            v
      Vehicle Control
            |
            v
        Telemetry
            |
            v
     Analysis Dashboard
```

---

## Key Features

### Vehicle Digital Twin

The virtual vehicle models simplified longitudinal vehicle behavior and operating state.

- Vehicle speed
- Acceleration
- Position
- Steering
- Throttle
- Braking
- Driving mode
- Battery State of Charge (SOC)
- Energy consumption
- Regenerative braking
- Tire condition model

### Simulated Automotive Sensors

The project contains modular sensor implementations:

| Sensor | Simulated Information |
|---|---|
| Radar | Object distance, relative speed, lateral position |
| Camera | Object detection, lane offset |
| Ultrasonic | Short-range object detection |
| IMU | Simplified yaw-rate information |
| GPS | Vehicle position |
| Wheel Speed | Vehicle wheel-speed measurement |

Each sensor follows a common abstraction, allowing individual sensors to be extended or replaced without changing the rest of the system.

### Sensor Fusion

The perception layer combines observations from multiple sensors into consolidated object estimates.

The fusion layer provides:

- Object association
- Distance estimation
- Relative-speed estimation
- Lateral-position estimation
- Confidence aggregation
- Sensor-source tracking

Example:

```text
Radar       -> Object A at 20.4 m
Camera      -> Object A at 21.1 m
Ultrasonic  -> Object A at 20.7 m
                    |
                    v
              Sensor Fusion
                    |
                    v
        Fused Object Estimate
        Distance: ~20.7 m
        Confidence: High
```

### ADAS Modules

AutoTwin currently implements five simplified ADAS functions.

| Module | Purpose |
|---|---|
| FCW | Forward Collision Warning |
| AEB | Automatic Emergency Braking |
| ACC | Adaptive Cruise Control |
| LDW | Lane Departure Warning |
| BSD | Blind Spot Detection |

#### Forward Collision Warning

FCW evaluates collision risk using a simplified Time-to-Collision calculation:

```text
TTC = Distance / Closing Speed
```

A warning is generated when the estimated TTC crosses the configured threshold.

#### Automatic Emergency Braking

AEB uses a more critical TTC threshold. When the simulated collision risk becomes severe, the vehicle commands maximum braking and switches to emergency mode.

#### Adaptive Cruise Control

ACC attempts to maintain a configurable target speed while reducing the commanded speed when a lead vehicle enters the following-distance region.

#### Lane Departure Warning

LDW monitors lateral lane offset and generates a warning when the simulated vehicle moves beyond the configured lane boundary.

#### Blind Spot Detection

BSD identifies nearby objects in lateral blind-spot regions and generates a warning when an object is detected.

---

## Simulation Scenarios

The project includes four predefined scenarios.

### Highway

Simulates highway driving with a lead vehicle and surrounding traffic.

```text
Vehicle -> Lead Vehicle -> Traffic
```

Used to demonstrate:

- Vehicle dynamics
- ACC
- Radar and camera perception
- Normal telemetry

### City

Simulates a lower-speed urban environment containing multiple road users.

Used to demonstrate:

- Multi-object perception
- Short-range sensing
- Urban driving conditions
- Sensor fusion

### Emergency Braking

Introduces a close obstacle in the vehicle path.

Expected behavior:

```text
Object Detection
      |
      v
     FCW
      |
      v
     AEB
      |
      v
Emergency Braking
```

This scenario is useful for demonstrating the safety pipeline.

### Lane Departure

Introduces steering behavior that moves the vehicle away from the lane center.

Expected behavior:

```text
Lane Offset
     |
     v
Threshold Exceeded
     |
     v
LDW Warning
```

---

## Dashboard

The project includes a Streamlit-based engineering dashboard for analyzing completed simulation runs.

### Vehicle

Displays:

- Vehicle speed
- Maximum speed
- Distance
- Battery SOC
- Acceleration
- Throttle
- Brake

### Perception

Displays:

- Sensor availability
- Closest detected object
- Fused object count
- Object-distance history

### ADAS

Displays:

- FCW events
- AEB events
- LDW events
- BSD events
- ADAS activity timeline
- Safety-event log

### Run Report

Displays:

- Scenario
- Simulation duration
- Final vehicle mode
- Complete telemetry
- Downloadable telemetry CSV

---

## Project Structure

```text
AutoTwin-ADAS/
|
+-- autotwin/
|   |
|   +-- core/
|   |   +-- enums.py
|   |   +-- models.py
|   |
|   +-- vehicle/
|   |   +-- components.py
|   |   +-- vehicle.py
|   |
|   +-- environment/
|   |   +-- world.py
|   |
|   +-- sensors/
|   |   +-- base.py
|   |   +-- sensor_suite.py
|   |
|   +-- perception/
|   |   +-- fusion.py
|   |
|   +-- adas/
|   |   +-- modules.py
|   |
|   +-- scenarios/
|   |   +-- scenarios.py
|   |
|   +-- simulation/
|   |   +-- engine.py
|   |
|   +-- factory.py
|   +-- cli.py
|
+-- dashboard/
|   +-- app.py
|
+-- config/
|   +-- default.json
|
+-- docs/
|   +-- ARCHITECTURE.md
|   +-- ADAS.md
|   +-- GETTING_STARTED.md
|   +-- ROADMAP.md
|
+-- scripts/
|   +-- run_all_demos.py
|
+-- tests/
|   +-- test_vehicle.py
|   +-- test_adas.py
|   +-- test_fusion.py
|   +-- test_simulation.py
|
+-- data/
|   +-- runs/
|
+-- .gitignore
+-- CONTRIBUTING.md
+-- LICENSE
+-- pyproject.toml
+-- requirements.txt
+-- README.md
```

---

## Object-Oriented Design

The project is intentionally structured around object-oriented programming principles.

### Abstraction

Common interfaces are defined for sensors and ADAS modules.

```text
Sensor
 |
 +-- RadarSensor
 +-- CameraSensor
 +-- UltrasonicSensor
 +-- IMUSensor
 +-- GPSSensor
 +-- WheelSpeedSensor
```

```text
ADASModule
 |
 +-- ForwardCollisionWarning
 +-- AutomaticEmergencyBraking
 +-- AdaptiveCruiseControl
 +-- LaneDepartureWarning
 +-- BlindSpotDetection
```

### Inheritance

Concrete sensors and ADAS modules inherit from their respective abstract base classes.

### Polymorphism

The simulation can work with different sensor and ADAS implementations through common interfaces.

### Composition

The vehicle is composed of independent components:

```text
Vehicle
 |
 +-- Battery
 +-- BrakeSystem
 +-- TireSystem
```

### Encapsulation

Vehicle state, component behavior, sensor behavior, and ADAS decision logic are separated into dedicated classes.

---

## Technology Stack

### Language

- Python 3.11+

### Core Libraries

- NumPy
- Pandas
- Streamlit
- Plotly
- Pytest

### Engineering Concepts

- Object-Oriented Programming
- Vehicle Simulation
- Vehicle Dynamics
- Sensor Simulation
- Sensor Fusion
- ADAS Logic
- Time-to-Collision
- Scenario-Based Testing
- Telemetry
- Data Visualization
- Automated Testing

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/AutoTwin-ADAS.git
cd AutoTwin-ADAS
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create a virtual environment

#### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

#### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Simulation

### Highway

```bash
python -m autotwin.cli --scenario highway --duration 30
```

### City

```bash
python -m autotwin.cli --scenario city --duration 30
```

### Emergency Braking

```bash
python -m autotwin.cli --scenario emergency_braking --duration 15
```

### Lane Departure

```bash
python -m autotwin.cli --scenario lane_departure --duration 20
```

Each simulation creates a run directory under:

```text
data/runs/
```

A completed run contains:

```text
telemetry.csv
events.json
summary.json
```

---

## Launching the Dashboard

After generating at least one simulation run:

```bash
streamlit run dashboard/app.py
```

The dashboard automatically reads available runs from:

```text
data/runs/
```

---

## Running All Demonstrations

To execute all predefined scenarios:

```bash
python scripts/run_all_demos.py
```

This runs:

```text
Highway
City
Emergency Braking
Lane Departure
```

and generates independent simulation results for each scenario.

---

## Testing

Run the complete test suite:

```bash
pytest -q
```

The test suite covers:

- Vehicle acceleration and braking
- ADAS collision-warning behavior
- AEB activation
- Sensor-fusion behavior
- Simulation telemetry generation

---

## Configuration

Default simulation parameters are stored in:

```text
config/default.json
```

Configuration includes:

- Vehicle mass
- Maximum speed
- Maximum acceleration
- Wheelbase
- Battery capacity
- Initial battery SOC
- Sensor ranges
- Sensor noise
- FCW TTC threshold
- AEB TTC threshold
- ACC target speed
- ACC following distance
- LDW lane-offset threshold
- BSD detection range

This allows simulation parameters to be changed without modifying the core implementation.

---

## Telemetry

Each simulation produces structured telemetry containing:

```text
timestamp
speed_kmh
acceleration_ms2
lane_offset_m
battery_soc
throttle
brake
closest_object_m
fused_objects
fcw
aeb
acc
ldw
bsd
```

This data can be used for:

- Simulation analysis
- Debugging
- ADAS evaluation
- Visualization
- Future machine-learning experiments

---

## Safety Event Logging

ADAS events are stored separately in:

```text
events.json
```

An event contains information such as:

```text
timestamp
module
severity
message
measured value
recommended action
```

Example event flow:

```text
FCW
Forward collision risk detected
        |
        v
AEB
Emergency braking triggered
        |
        v
Vehicle enters EMERGENCY mode
```

Repeated identical alerts are rate-limited in the event log so that the generated safety report remains readable while the simulation control logic continues operating.

---

## Validation

The final project includes automated tests and scenario validation.

The test suite validates:

- Vehicle dynamics
- Emergency braking behavior
- FCW
- AEB
- Sensor fusion
- Simulation telemetry

The demonstration suite validates:

```text
Highway
City
Emergency Braking
Lane Departure
```

The emergency-braking scenario is specifically designed to demonstrate the FCW-to-AEB safety path.

---

## Design Goals

The project was designed with the following principles:

1. **Modularity**  
   Automotive components are separated into independent packages.

2. **Extensibility**  
   New sensors, ADAS modules, scenarios, and perception algorithms can be added without redesigning the entire system.

3. **Testability**  
   Core components can be tested independently.

4. **Configurability**  
   Important simulation parameters are stored outside the implementation.

5. **Separation of Concerns**  
   Simulation logic, perception, ADAS, telemetry, and visualization remain independent.

6. **Automotive Relevance**  
   The architecture reflects common conceptual stages in an automotive perception and ADAS pipeline.

---

## Limitations

AutoTwin ADAS is intentionally simplified.

It does not currently provide:

- Real radar hardware integration
- Real camera hardware integration
- Production-grade computer vision
- Real-time operating-system behavior
- AUTOSAR integration
- Functional-safety certification
- ISO 26262 compliance
- Real vehicle CAN communication
- Production vehicle dynamics
- Production-grade object tracking
- Safety-certified control algorithms

The current sensors generate synthetic measurements and the ADAS algorithms are educational approximations.

---



## Future Architecture

The long-term direction of the project is:

```text
                Real / Simulated Sensors
                         |
             +-----------+-----------+
             |           |           |
           Radar       Camera    Ultrasonic
             |           |           |
             +-----------+-----------+
                         |
                         v
                 Sensor Fusion
                         |
                         v
                 Object Tracking
                         |
                         v
                Scene Understanding
                         |
                         v
                   ADAS Layer
                         |
          +--------------+--------------+
          |              |              |
         FCW            AEB            ACC
          |              |              |
          +--------------+--------------+
                         |
                         v
                  Vehicle Control
                         |
                         v
                   Digital Twin
```

The current project provides the software foundation for this future architecture.

---

## Learning Outcomes

This project provides practical experience with:

- Python object-oriented programming
- Software architecture
- Abstract classes and interfaces
- Inheritance and polymorphism
- Composition
- Simulation loops
- Automotive sensor concepts
- Sensor fusion
- ADAS decision logic
- Time-to-Collision
- Vehicle dynamics
- Telemetry pipelines
- Data visualization
- Automated testing
- Modular project design

---

