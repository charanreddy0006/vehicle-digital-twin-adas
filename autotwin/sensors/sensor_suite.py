import math
from .base import Sensor
from ..core.models import SensorFrame, DetectedObject

class RadarSensor(Sensor):
    def __init__(self, range_m=160, noise_std=0.03):
        super().__init__("radar", range_m, noise_std)

    def read(self, vehicle, world, rng):
        objects = []
        for obj, dx, dy in world.relative_objects(vehicle.state.x_m, vehicle.state.y_m):
            distance = math.hypot(dx, dy)
            if distance <= self.range_m:
                measured = max(0.1, distance + rng.gauss(0, self.noise_std * max(distance, 1)))
                objects.append(DetectedObject(
                    obj.object_id, obj.object_type, measured,
                    obj.speed_ms - vehicle.state.speed_ms, dy,
                    max(0.5, 1 - distance / self.range_m), self.name
                ))
        return SensorFrame(vehicle.state.time_s, self.name, objects=objects)

class CameraSensor(Sensor):
    def __init__(self, range_m=100, noise_std=0.03):
        super().__init__("camera", range_m, noise_std)

    def read(self, vehicle, world, rng):
        objects = []
        for obj, dx, dy in world.relative_objects(vehicle.state.x_m, vehicle.state.y_m):
            distance = math.hypot(dx, dy)
            if distance <= self.range_m and abs(dy) < 7:
                measured = max(0.1, distance + rng.gauss(0, self.noise_std * max(distance, 1)))
                objects.append(DetectedObject(
                    obj.object_id, obj.object_type, measured,
                    obj.speed_ms - vehicle.state.speed_ms, dy,
                    max(0.55, 1 - distance / self.range_m), self.name
                ))
        lane_offset = vehicle.state.lane_offset_m + rng.gauss(0, self.noise_std)
        return SensorFrame(vehicle.state.time_s, self.name, objects, lane_offset_m=lane_offset)

class UltrasonicSensor(Sensor):
    def __init__(self, range_m=8, noise_std=0.03):
        super().__init__("ultrasonic", range_m, noise_std)

    def read(self, vehicle, world, rng):
        objects = []
        for obj, dx, dy in world.relative_objects(vehicle.state.x_m, vehicle.state.y_m):
            distance = math.hypot(dx, dy)
            if distance <= self.range_m:
                objects.append(DetectedObject(
                    obj.object_id, obj.object_type, distance,
                    obj.speed_ms - vehicle.state.speed_ms, dy, 0.9, self.name
                ))
        return SensorFrame(vehicle.state.time_s, self.name, objects=objects)

class IMUSensor(Sensor):
    def __init__(self):
        super().__init__("imu", 0)

    def read(self, vehicle, world, rng):
        yaw_rate = vehicle.state.steering_deg * vehicle.state.speed_ms * 0.15
        return SensorFrame(vehicle.state.time_s, self.name, yaw_rate_dps=yaw_rate)

class GPSSensor(Sensor):
    def __init__(self, noise_std=0.03):
        super().__init__("gps", 0, noise_std)

    def read(self, vehicle, world, rng):
        return SensorFrame(
            vehicle.state.time_s, self.name,
            gps_x_m=vehicle.state.x_m + rng.gauss(0, self.noise_std),
            gps_y_m=vehicle.state.y_m + rng.gauss(0, self.noise_std),
        )

class WheelSpeedSensor(Sensor):
    def __init__(self):
        super().__init__("wheel_speed", 0)

    def read(self, vehicle, world, rng):
        return SensorFrame(
            vehicle.state.time_s, self.name,
            wheel_speed_ms=vehicle.state.speed_ms
        )

class SensorSuite:
    def __init__(self, sensors):
        self.sensors = sensors

    def read_all(self, vehicle, world, rng):
        return [
            sensor.read(vehicle, world, rng)
            for sensor in self.sensors
            if sensor.enabled
        ]
