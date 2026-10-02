import argparse
from datetime import datetime
from pathlib import Path

from .factory import create_system
from .simulation.engine import SimulationEngine
from .scenarios.scenarios import apply_scenario_behavior

def main():
    parser = argparse.ArgumentParser(
        description="AutoTwin — Vehicle Digital Twin + ADAS simulator"
    )
    parser.add_argument(
        "--scenario",
        choices=["highway", "city", "emergency_braking", "lane_departure"],
        default="highway",
    )
    parser.add_argument("--duration", type=float, default=30)
    parser.add_argument("--dt", type=float, default=0.1)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    vehicle, world, sensors, fusion, adas = create_system(scenario=args.scenario)

    engine = SimulationEngine(
        vehicle, world, sensors, fusion, adas, args.scenario, args.seed
    )
    engine.run(args.duration, args.dt, apply_scenario_behavior)

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output = engine.save_run(Path("data/runs") / f"{stamp}_{args.scenario}")

    print("\n" + "=" * 55)
    print("🚗 AUTOTWIN ADAS — SIMULATION COMPLETE")
    print("=" * 55)
    print(f"Scenario       : {args.scenario}")
    print(f"Duration       : {vehicle.state.time_s:.1f} s")
    print(f"Distance       : {vehicle.state.x_m:.1f} m")
    print(f"Max speed      : {max((r.speed_kmh for r in engine.records), default=0):.1f} km/h")
    print(f"Battery SOC    : {vehicle.state.battery_soc * 100:.1f}%")
    print(f"Safety events  : {len(engine.events)}")
    print(f"FCW / AEB      : {sum(e.module == 'FCW' for e in engine.events)} / {sum(e.module == 'AEB' for e in engine.events)}")
    print(f"LDW / BSD      : {sum(e.module == 'LDW' for e in engine.events)} / {sum(e.module == 'BSD' for e in engine.events)}")
    print(f"Output         : {output.resolve()}")
    print("=" * 55)

if __name__ == "__main__":
    main()
