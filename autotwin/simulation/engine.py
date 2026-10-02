import csv
import json
from pathlib import Path
import random
from ..core.models import TelemetryRecord
from ..sensors.sensor_suite import SensorSuite
class SimulationEngine:
    def __init__(self, vehicle, world, sensors, fusion, adas, scenario_name="custom", seed=42):
        self.vehicle = vehicle
        self.world = world
        self.sensors = sensors
        self.fusion = fusion
        self.adas = adas
        self.scenario_name = scenario_name
        self.rng = random.Random(seed)
        self.records = []
        self.events = []
        self.sensor_status = {s.name: "ONLINE" for s in sensors.sensors}
        self._last_logged_event_time = {}
        self.event_log_cooldown_s = 1.0

    def step(self, dt_s=0.1):
        frames = self.sensors.read_all(self.vehicle, self.world, self.rng)
        fused_objects = self.fusion.fuse(frames)
        lane_offset = self.fusion.lane_offset(frames)

        events = self.adas.evaluate(
            self.vehicle, fused_objects, lane_offset, self.world
        )

        # Keep control behavior continuous, but avoid writing the same alert
        # every 100 ms to the safety event log.
        for event in events:
            last_time = self._last_logged_event_time.get(event.module, -999.0)
            if event.timestamp - last_time >= self.event_log_cooldown_s:
                self.events.append(event)
                self._last_logged_event_time[event.module] = event.timestamp

        self.vehicle.update(dt_s)
        self.world.update(dt_s)

        closest = min(
            (o.distance_m for o in fused_objects if o.distance_m > 0),
            default=999.0
        )
        active = {e.module for e in events}

        self.records.append(TelemetryRecord(
            timestamp=self.vehicle.state.time_s,
            speed_kmh=self.vehicle.speed_kmh,
            acceleration_ms2=self.vehicle.state.acceleration_ms2,
            lane_offset_m=self.vehicle.state.lane_offset_m,
            battery_soc=self.vehicle.state.battery_soc,
            throttle=self.vehicle.state.throttle,
            brake=self.vehicle.state.brake,
            closest_object_m=closest,
            fused_objects=len(fused_objects),
            fcw=int("FCW" in active),
            aeb=int("AEB" in active),
            acc=int(self.vehicle.state.mode.value == "ADAS"),
            ldw=int("LDW" in active),
            bsd=int("BSD" in active),
        ))

        return events, fused_objects

    def run(self, duration_s=30, dt_s=0.1, scenario_behavior=None):
        steps = int(duration_s / dt_s)
        for _ in range(steps):
            if scenario_behavior:
                scenario_behavior(self.scenario_name, self.world, self.vehicle)
            self.step(dt_s)
        return self.records

    def save_run(self, output_dir):
        path = Path(output_dir)
        path.mkdir(parents=True, exist_ok=True)

        with (path / "telemetry.csv").open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f, fieldnames=TelemetryRecord.__dataclass_fields__.keys()
            )
            writer.writeheader()
            for record in self.records:
                writer.writerow(record.__dict__)

        events = [
            {
                **event.__dict__,
                "level": event.level.value
            }
            for event in self.events
        ]
        (path / "events.json").write_text(
            json.dumps(events, indent=2), encoding="utf-8"
        )

        summary = {
            "project": "AutoTwin ADAS",
            "version": "2.0.0",
            "scenario": self.scenario_name,
            "duration_s": round(self.vehicle.state.time_s, 2),
            "distance_m": round(self.vehicle.state.x_m, 2),
            "max_speed_kmh": round(max((r.speed_kmh for r in self.records), default=0), 2),
            "final_battery_soc": round(self.vehicle.state.battery_soc, 4),
            "final_mode": self.vehicle.state.mode.value,
            "events": len(self.events),
            "fcw_events": sum(e.module == "FCW" for e in self.events),
            "aeb_events": sum(e.module == "AEB" for e in self.events),
            "ldw_events": sum(e.module == "LDW" for e in self.events),
            "bsd_events": sum(e.module == "BSD" for e in self.events),
        }
        (path / "summary.json").write_text(
            json.dumps(summary, indent=2), encoding="utf-8"
        )
        return path
