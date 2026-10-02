from typing import Any


def validate_simulation_config(config: dict[str, Any]) -> None:
    """Validate the vehicle, sensor, and ADAS configuration."""

    # Validate vehicle configuration
    vehicle = config.get("vehicle")

    if not vehicle:
        raise ValueError("Vehicle configuration is missing.")

    mass = vehicle.get("mass_kg", 0)
    max_speed = vehicle.get("max_speed_kmh", 0)
    max_acceleration = vehicle.get("max_acceleration_ms2", 0)
    wheelbase = vehicle.get("wheelbase_m", 0)
    battery_capacity = vehicle.get("battery_capacity_kwh", 0)
    initial_soc = vehicle.get("initial_soc", -1)

    if mass <= 0:
        raise ValueError("Vehicle mass must be greater than 0.")

    if max_speed <= 0:
        raise ValueError("Vehicle maximum speed must be greater than 0.")

    if max_acceleration <= 0:
        raise ValueError(
            "Vehicle maximum acceleration must be greater than 0."
        )

    if wheelbase <= 0:
        raise ValueError("Vehicle wheelbase must be greater than 0.")

    if battery_capacity <= 0:
        raise ValueError(
            "Battery capacity must be greater than 0."
        )

    if not 0 <= initial_soc <= 1:
        raise ValueError(
            "Initial battery SOC must be between 0 and 1."
        )

    # Validate sensor configuration
    sensors = config.get("sensors")

    if not sensors:
        raise ValueError("Sensor configuration is missing.")

    sensor_ranges = (
        "radar_range_m",
        "camera_range_m",
        "ultrasonic_range_m",
    )

    for sensor_range in sensor_ranges:
        value = sensors.get(sensor_range, 0)

        if value <= 0:
            raise ValueError(
                f"{sensor_range} must be greater than 0."
            )

    noise_std = sensors.get("noise_std", 0)

    if noise_std < 0:
        raise ValueError("Sensor noise standard deviation cannot be negative.")

    # Validate ADAS configuration
    adas = config.get("adas")

    if not adas:
        raise ValueError("ADAS configuration is missing.")

    thresholds = (
        "fcw_ttc_s",
        "aeb_ttc_s",
        "acc_follow_distance_m",
        "bsd_range_m",
    )

    for threshold in thresholds:
        value = adas.get(threshold, 0)

        if value <= 0:
            raise ValueError(
                f"{threshold} must be greater than 0."
            )

    if adas.get("ldw_threshold_m", 0) <= 0:
        raise ValueError(
            "ldw_threshold_m must be greater than 0."
        )

    if adas["aeb_ttc_s"] > adas["fcw_ttc_s"]:
        raise ValueError(
            "AEB TTC threshold should not be greater than FCW TTC threshold."
        )