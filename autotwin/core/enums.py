from enum import Enum

class VehicleMode(str, Enum):
    PARKED = "PARKED"
    MANUAL = "MANUAL"
    ADAS = "ADAS"
    EMERGENCY = "EMERGENCY"

class AlertLevel(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"

class ObjectType(str, Enum):
    VEHICLE = "vehicle"
    PEDESTRIAN = "pedestrian"
    OBSTACLE = "obstacle"
    UNKNOWN = "unknown"
