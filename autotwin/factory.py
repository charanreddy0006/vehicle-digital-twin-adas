import json
from pathlib import Path

from .core.validation import validate_simulation_config

from .vehicle.vehicle import Vehicle
from .sensors.sensor_suite import (
    SensorSuite,
    RadarSensor,
    CameraSensor,
    UltrasonicSensor,
    IMUSensor,
    GPSSensor,
    WheelSpeedSensor,
)
from .perception.fusion import SensorFusion
from .adas.modules import (
    ADASController,
    ForwardCollisionWarning,
    AutomaticEmergencyBraking,
    AdaptiveCruiseControl,
    LaneDepartureWarning,
    BlindSpotDetection,
)
from .scenarios.scenarios import create_scenario


def load_config(path="config/default.json"):
    candidate = Path(path)

    if not candidate.is_absolute() and not candidate.exists():
        candidate = Path(__file__).resolve().parents[1] / path

    return json.loads(candidate.read_text(encoding="utf-8"))


def create_system(config_path="config/default.json", scenario="highway"):
    if config_path in {
        "highway",
        "city",
        "emergency_braking",
        "lane_departure",
    }:
        scenario = config_path
        config_path = "config/default.json"

    cfg = load_config(config_path)

    # Validate the simulation configuration before creating the system.
    validate_simulation_config(cfg)

    v = cfg["vehicle"]
    s = cfg["sensors"]
    a = cfg["adas"]

    vehicle = Vehicle(
        mass_kg=v["mass_kg"],
        max_speed_kmh=v["max_speed_kmh"],
        max_acceleration_ms2=v["max_acceleration_ms2"],
        wheelbase_m=v["wheelbase_m"],
        battery_capacity_kwh=v["battery_capacity_kwh"],
        initial_soc=v["initial_soc"],
    )

    sensors = SensorSuite([
        RadarSensor(
            s["radar_range_m"],
            s["noise_std"],
        ),
        CameraSensor(
            s["camera_range_m"],
            s["noise_std"],
        ),
        UltrasonicSensor(
            s["ultrasonic_range_m"],
            s["noise_std"],
        ),
        IMUSensor(),
        GPSSensor(s["noise_std"]),
        WheelSpeedSensor(),
    ])

    fusion = SensorFusion(
        distance_gate_m=6.0
    )

    adas = ADASController([
        ForwardCollisionWarning(
            a["fcw_ttc_s"]
        ),
        AutomaticEmergencyBraking(
            a["aeb_ttc_s"]
        ),
        AdaptiveCruiseControl(
            a["acc_target_speed_kmh"],
            a["acc_follow_distance_m"],
        ),
        LaneDepartureWarning(
            a["ldw_threshold_m"]
        ),
        BlindSpotDetection(
            a["bsd_range_m"]
        ),
    ])

    return (
        vehicle,
        create_scenario(scenario),
        sensors,
        fusion,
        adas,
    )