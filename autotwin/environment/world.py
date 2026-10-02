from dataclasses import dataclass
from ..core.enums import ObjectType

@dataclass
class WorldObject:
    object_id: str
    object_type: ObjectType
    x_m: float
    y_m: float
    speed_ms: float
    width_m: float = 1.8

class RoadWorld:
    def __init__(self, lane_width_m=3.6):
        self.lane_width_m = lane_width_m
        self.speed_limit_kmh = 100.0
        self.objects: list[WorldObject] = []

    def add_object(self, obj: WorldObject):
        self.objects.append(obj)

    def update(self, dt_s: float):
        for obj in self.objects:
            obj.x_m += obj.speed_ms * dt_s

    def relative_objects(self, vehicle_x: float, vehicle_y: float):
        result = []
        for obj in self.objects:
            dx = obj.x_m - vehicle_x
            dy = obj.y_m - vehicle_y
            if dx > -5:
                result.append((obj, dx, dy))
        return result
