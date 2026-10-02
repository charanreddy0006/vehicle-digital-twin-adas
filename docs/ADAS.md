# ADAS Design

## FCW — Forward Collision Warning

Uses Time-to-Collision:

```text
TTC = distance / closing_speed
```

A warning is emitted when TTC is below the configured threshold.

## AEB — Automatic Emergency Braking

Uses a lower TTC threshold than FCW. The simulation commands maximum braking when the threshold is crossed.

## ACC — Adaptive Cruise Control

Maintains a target speed while reducing commanded speed when a lead object enters the configured following-distance region.

## LDW — Lane Departure Warning

Uses lateral lane offset and generates a warning beyond the configured threshold.

## BSD — Blind Spot Detection

Detects nearby objects laterally offset from the primary lane.

## Sensor Fusion

Radar and camera observations are grouped by object identity and combined using confidence-weighted measurements.

All algorithms are simplified educational models and do not represent production ADAS implementations.
