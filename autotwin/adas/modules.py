from abc import ABC, abstractmethod
from ..core.enums import AlertLevel, VehicleMode
from ..core.models import SafetyEvent, FusedObject

class ADASModule(ABC):
    name = "ADAS"

    @abstractmethod
    def evaluate(self, vehicle, fused_objects: list[FusedObject], lane_offset, world):
        ...

def front_objects(objects):
    return [
        o for o in objects
        if abs(o.lateral_offset_m) < 1.8 and o.distance_m > 0
    ]

class ForwardCollisionWarning(ADASModule):
    name = "FCW"

    def __init__(self, ttc_threshold=3.0):
        self.ttc_threshold = ttc_threshold

    def evaluate(self, vehicle, fused_objects, lane_offset, world):
        candidates = front_objects(fused_objects)
        if not candidates:
            return None
        obj = min(candidates, key=lambda x: x.distance_m)
        closing = max(0.1, -obj.relative_speed_ms)
        ttc = obj.distance_m / closing
        if ttc <= self.ttc_threshold:
            return SafetyEvent(
                vehicle.state.time_s, self.name, AlertLevel.WARNING,
                f"Forward collision risk: {obj.object_id}",
                ttc, "Reduce speed / prepare to brake"
            )

class AutomaticEmergencyBraking(ADASModule):
    name = "AEB"

    def __init__(self, ttc_threshold=1.5):
        self.ttc_threshold = ttc_threshold

    def evaluate(self, vehicle, fused_objects, lane_offset, world):
        candidates = front_objects(fused_objects)
        if not candidates:
            return None
        obj = min(candidates, key=lambda x: x.distance_m)
        closing = max(0.1, -obj.relative_speed_ms)
        ttc = obj.distance_m / closing
        if ttc <= self.ttc_threshold:
            vehicle.emergency_brake()
            return SafetyEvent(
                vehicle.state.time_s, self.name, AlertLevel.CRITICAL,
                f"Emergency braking triggered for {obj.object_id}",
                ttc, "Apply maximum braking"
            )

class AdaptiveCruiseControl(ADASModule):
    name = "ACC"

    def __init__(self, target_speed_kmh=90, follow_distance_m=35):
        self.target_speed_ms = target_speed_kmh / 3.6
        self.follow_distance_m = follow_distance_m

    def evaluate(self, vehicle, fused_objects, lane_offset, world):
        if vehicle.state.mode == VehicleMode.EMERGENCY:
            return None

        desired_speed = min(self.target_speed_ms, world.speed_limit_kmh / 3.6)
        candidates = front_objects(fused_objects)

        if candidates:
            obj = min(candidates, key=lambda x: x.distance_m)
            if obj.distance_m < self.follow_distance_m + 10:
                desired_speed = min(
                    desired_speed,
                    max(0.0, vehicle.state.speed_ms + obj.relative_speed_ms)
                )

        error = desired_speed - vehicle.state.speed_ms
        throttle = max(0.0, min(1.0, error / 7.0))
        brake = max(0.0, min(1.0, -error / 5.0))

        vehicle.set_controls(throttle, brake, vehicle.state.steering_deg)
        vehicle.state.mode = VehicleMode.ADAS
        return None

class LaneDepartureWarning(ADASModule):
    name = "LDW"

    def __init__(self, threshold_m=0.45):
        self.threshold_m = threshold_m

    def evaluate(self, vehicle, fused_objects, lane_offset, world):
        if lane_offset is not None and abs(lane_offset) >= self.threshold_m:
            return SafetyEvent(
                vehicle.state.time_s, self.name, AlertLevel.WARNING,
                f"Lane departure detected: offset={lane_offset:.2f}m",
                lane_offset, "Correct steering"
            )

class BlindSpotDetection(ADASModule):
    name = "BSD"

    def __init__(self, range_m=12):
        self.range_m = range_m

    def evaluate(self, vehicle, fused_objects, lane_offset, world):
        side = [
            o for o in fused_objects
            if 1.8 <= abs(o.lateral_offset_m) <= 5.5 and o.distance_m <= self.range_m
        ]
        if side:
            obj = min(side, key=lambda x: x.distance_m)
            return SafetyEvent(
                vehicle.state.time_s, self.name, AlertLevel.WARNING,
                f"Object in blind spot: {obj.object_id}",
                obj.distance_m, "Avoid lane change"
            )

class ADASController:
    def __init__(self, modules):
        self.modules = modules

    def evaluate(self, vehicle, fused_objects, lane_offset, world):
        events = []
        for module in self.modules:
            event = module.evaluate(vehicle, fused_objects, lane_offset, world)
            if event:
                events.append(event)
        return events
