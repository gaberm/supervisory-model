from abc import ABC, abstractmethod
from dataclasses import dataclass


class ModelAdapter(ABC):
    def __init__(self, name: str, timestep_length: float):
        self.name = name
        self.timestep_length = timestep_length
        self.current_time = 0.0

    @property
    @abstractmethod
    def current_time(self) -> float:
        """Return the current simulation time."""
        pass

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def read_outputs(self) -> dataclass:
        pass

    @abstractmethod
    def write_inputs(self, inputs: dataclass):
        pass

    @abstractmethod
    def advance(self, dt: float):
        pass
