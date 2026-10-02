import math
from ..core.enums import VehicleMode
from ..core.models import VehicleState
from .components import Battery, BrakeSystem, TireSystem

class Vehicle:
    """Simplified EV digital twin with longitudinal dynamics."""

    def __init__(
        self,
        mass_kg=1650,
        max_speed_kmh=180,
        max_acceleration_ms2=4.0,
        wheelbase_m=2.7,
        battery_capacity_kwh=62.0,
        initial_soc=0.82,
    ):
        self.mass_kg = mass_kg
        self.max_speed_ms = max_speed_kmh / 3.6
        self.max_acceleration_ms2 = max_acceleration_ms2
        self.wheelbase_m = wheelbase_m
        self.state = VehicleState(battery_soc=initial_soc)
        self.battery = Battery(battery_capacity_kwh, initial_soc)
        self.brakes = BrakeSystem()
        self.tires = TireSystem()

    def set_controls(self, throttle: float, brake: float, steering_deg: float = 0.0):
        self.state.throttle = max(0.0, min(1.0, throttle))
        self.state.brake = max(0.0, min(1.0, brake))
        self.state.steering_deg = max(-35.0, min(35.0, steering_deg))

    def update(self, dt_s: float):
        s = self.state

        drive_acc = self.max_acceleration_ms2 * s.throttle
        brake_acc = self.brakes.braking_acceleration(s.brake)

        aerodynamic_drag = 0.012 * s.speed_ms**2 / max(self.mass_kg / 1000, 1)
        s.acceleration_ms2 = drive_acc + brake_acc - aerodynamic_drag

        s.speed_ms = max(
            0.0,
            min(self.max_speed_ms, s.speed_ms + s.acceleration_ms2 * dt_s),
        )

        if s.speed_ms > 0.1:
            steering_rad = math.radians(s.steering_deg)
            yaw_rate_rad = s.speed_ms / self.wheelbase_m * math.tan(steering_rad)
            heading = yaw_rate_rad * dt_s
        else:
            heading = 0.0

        s.x_m += s.speed_ms * math.cos(heading) * dt_s
        s.y_m += s.speed_ms * math.sin(heading) * dt_s
        s.lane_offset_m = s.y_m

        traction_power_kw = max(
            0.0,
            8.0 + 0.25 * s.speed_ms**2 + 35.0 * s.throttle,
        )

        if s.acceleration_ms2 < -0.5:
            self.battery.regenerate(min(25.0, abs(s.acceleration_ms2) * 3), dt_s)
        else:
            self.battery.consume(traction_power_kw, dt_s)

        s.battery_soc = self.battery.soc
        s.energy_kwh += max(0.0, traction_power_kw) * dt_s / 3600
        s.time_s += dt_s

    @property
    def speed_ms(self):
        return self.state.speed_ms

    @property
    def speed_kmh(self):
        return self.state.speed_ms * 3.6

    def emergency_brake(self):
        self.state.mode = VehicleMode.EMERGENCY
        self.set_controls(0.0, 1.0, self.state.steering_deg)
