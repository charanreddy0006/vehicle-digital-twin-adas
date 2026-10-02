from dataclasses import dataclass, field
from typing import Optional
from .enums import ObjectType, AlertLevel, VehicleMode

@dataclass
class VehicleState:
    time_s: float = 0.0
    x_m: float = 0.0
    y_m: float = 0.0
    speed_ms: float = 0.0
    acceleration_ms2: float = 0.0
    steering_deg: float = 0.0
    throttle: float = 0.0
    brake: float = 0.0
    lane_offset_m: float = 0.0
    battery_soc: float = 0.82
    energy_kwh: float = 0.0
    mode: VehicleMode = VehicleMode.MANUAL

@dataclass
class DetectedObject:
    object_id: str
    object_type: ObjectType
    distance_m: float
    relative_speed_ms: float
    lateral_offset_m: float
    confidence: float
    source: str

@dataclass
class FusedObject:
    object_id: str
    object_type: ObjectType
    distance_m: float
    relative_speed_ms: float
    lateral_offset_m: float
    confidence: float
    sources: list[str] = field(default_factory=list)

@dataclass
class SensorFrame:
    timestamp: float
    sensor_name: str
    objects: list[DetectedObject] = field(default_factory=list)
    lane_offset_m: Optional[float] = None
    wheel_speed_ms: Optional[float] = None
    yaw_rate_dps: Optional[float] = None
    gps_x_m: Optional[float] = None
    gps_y_m: Optional[float] = None

@dataclass
class SafetyEvent:
    timestamp: float
    module: str
    level: AlertLevel
    message: str
    value: float | None = None
    recommended_action: str = ""

@dataclass
class TelemetryRecord:
    timestamp: float
    speed_kmh: float
    acceleration_ms2: float
    lane_offset_m: float
    battery_soc: float
    throttle: float
    brake: float
    closest_object_m: float
    fused_objects: int
    fcw: int
    aeb: int
    acc: int
    ldw: int
    bsd: int
