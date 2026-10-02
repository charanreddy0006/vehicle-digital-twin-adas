from autotwin.vehicle.vehicle import Vehicle
from autotwin.environment.world import RoadWorld
from autotwin.core.enums import ObjectType
from autotwin.core.models import FusedObject
from autotwin.adas.modules import ForwardCollisionWarning, AutomaticEmergencyBraking

def make_object(distance=20, relative_speed=-10):
    return FusedObject(
        "lead", ObjectType.VEHICLE, distance, relative_speed, 0, 0.9, ["radar", "camera"]
    )

def test_fcw_triggers():
    vehicle = Vehicle()
    vehicle.state.speed_ms = 20
    event = ForwardCollisionWarning(3).evaluate(
        vehicle, [make_object(20, -10)], None, RoadWorld()
    )
    assert event is not None
    assert event.module == "FCW"

def test_aeb_triggers():
    vehicle = Vehicle()
    vehicle.state.speed_ms = 20
    event = AutomaticEmergencyBraking(1.5).evaluate(
        vehicle, [make_object(5, -10)], None, RoadWorld()
    )
    assert event is not None
    assert event.module == "AEB"
    assert vehicle.state.brake == 1.0
