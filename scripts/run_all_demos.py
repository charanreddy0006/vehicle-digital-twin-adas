from datetime import datetime
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from autotwin.factory import create_system
from autotwin.simulation.engine import SimulationEngine
from autotwin.scenarios.scenarios import apply_scenario_behavior

for scenario in ["highway", "city", "emergency_braking", "lane_departure"]:
    vehicle, world, sensors, fusion, adas = create_system(scenario=scenario)
    engine = SimulationEngine(
        vehicle, world, sensors, fusion, adas, scenario
    )
    engine.run(15, 0.1, apply_scenario_behavior)

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output = engine.save_run(Path("data/runs") / f"{stamp}_{scenario}")
    print(f"Completed {scenario}: {output}")
