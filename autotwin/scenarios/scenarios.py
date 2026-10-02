from ..environment.world import RoadWorld, WorldObject
from ..core.enums import ObjectType

def create_scenario(name: str):
    world = RoadWorld()

    if name == "highway":
        world.speed_limit_kmh = 100
        world.add_object(WorldObject("lead_car", ObjectType.VEHICLE, 70, 0, 22))
        world.add_object(WorldObject("right_car", ObjectType.VEHICLE, 55, 3.8, 24))
        return world

    if name == "city":
        world.speed_limit_kmh = 50
        world.add_object(WorldObject("city_car", ObjectType.VEHICLE, 42, 0, 10))
        world.add_object(WorldObject("pedestrian", ObjectType.PEDESTRIAN, 65, 3.0, 1.2, 0.6))
        world.add_object(WorldObject("side_car", ObjectType.VEHICLE, 32, -4.0, 12))
        return world

    if name == "emergency_braking":
        world.speed_limit_kmh = 80
        world.add_object(WorldObject("slow_vehicle", ObjectType.VEHICLE, 50, 0, 0))
        return world

    if name == "lane_departure":
        world.speed_limit_kmh = 80
        return world

    raise ValueError(f"Unknown scenario: {name}")

def apply_scenario_behavior(name, world, vehicle):
    if name == "emergency_braking" and vehicle.state.time_s > 4:
        for obj in world.objects:
            if obj.object_id == "slow_vehicle":
                # Deterministic close obstacle for demonstrating FCW/AEB.
                obj.x_m = vehicle.state.x_m + 1.5
                obj.speed_ms = 0
                if vehicle.state.speed_ms < 8.0:
                    vehicle.state.speed_ms = 8.0

    if name == "lane_departure" and 3 < vehicle.state.time_s < 8:
        vehicle.set_controls(0.35, 0.0, 10)
    elif name == "lane_departure" and 8 <= vehicle.state.time_s < 12:
        vehicle.set_controls(0.15, 0.0, -10)
