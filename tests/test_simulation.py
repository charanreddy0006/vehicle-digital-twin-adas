from autotwin.factory import create_system
from autotwin.simulation.engine import SimulationEngine
from autotwin.scenarios.scenarios import apply_scenario_behavior

def test_simulation_generates_telemetry():
    vehicle, world, sensors, fusion, adas = create_system("highway")
    engine = SimulationEngine(vehicle, world, sensors, fusion, adas, "highway")
    records = engine.run(2, 0.1, apply_scenario_behavior)
    assert len(records) == 20
    assert records[-1].timestamp > 0
    assert records[-1].fused_objects >= 0
