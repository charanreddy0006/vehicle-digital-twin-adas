from autotwin.vehicle.vehicle import Vehicle

def test_vehicle_accelerates():
    vehicle = Vehicle()
    vehicle.set_controls(1.0, 0.0)
    for _ in range(20):
        vehicle.update(0.1)
    assert vehicle.speed_ms > 0

def test_emergency_brake():
    vehicle = Vehicle()
    vehicle.state.speed_ms = 20
    vehicle.emergency_brake()
    assert vehicle.state.brake == 1.0
    assert vehicle.state.mode.value == "EMERGENCY"
