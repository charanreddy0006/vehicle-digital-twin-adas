from abc import ABC, abstractmethod
from ..core.models import SensorFrame

class Sensor(ABC):
    def __init__(self, name: str, range_m: float, noise_std: float = 0.03):
        self.name = name
        self.range_m = range_m
        self.noise_std = noise_std
        self.enabled = True

    @abstractmethod
    def read(self, vehicle, world, rng) -> SensorFrame:
        ...
