from dataclasses import dataclass

@dataclass
class Battery:
    capacity_kwh: float
    soc: float

    def consume(self, power_kw: float, dt_s: float) -> None:
        if power_kw > 0:
            self.soc = max(0.0, self.soc - (power_kw * dt_s / 3600) / self.capacity_kwh)

    def regenerate(self, power_kw: float, dt_s: float) -> None:
        if power_kw > 0:
            self.soc = min(1.0, self.soc + (power_kw * dt_s / 3600) / self.capacity_kwh)

@dataclass
class BrakeSystem:
    max_deceleration_ms2: float = 8.5

    def braking_acceleration(self, brake: float) -> float:
        return -max(0.0, min(1.0, brake)) * self.max_deceleration_ms2

@dataclass
class TireSystem:
    front_pressure_psi: float = 35.0
    rear_pressure_psi: float = 35.0

    def health_score(self) -> float:
        avg_deviation = (
            abs(self.front_pressure_psi - 35.0)
            + abs(self.rear_pressure_psi - 35.0)
        ) / 2
        return max(0.0, 100.0 - avg_deviation * 8)
