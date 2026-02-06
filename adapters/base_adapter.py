from abc import ABC, abstractmethod
from dataclasses import dataclass
from literalai import Optional


class BaseAdapter(ABC):
    InputType: type[dataclass] = None
    OutputType: type[dataclass] = None

    def __init__(self, name: str, timestep_length: Optional[float] = None):
        self.name = name
        self.timestep_length = timestep_length
        self.model_time = 0.0

    @property
    def model_time(self) -> float:
        """Return the model's current simulation time in global time units."""
        return self.model_time

    @property
    def timestep_length(self) -> float:
        """Return the model's timestep length in global time units."""
        if self.timestep_length is None:
            raise ValueError("timestep_length not set.")
        return self.timestep_length

    @abstractmethod
    def initialize(self):
        """Initialize the model."""
        pass

    @abstractmethod
    def read_outputs(self) -> dataclass:
        pass

    @abstractmethod
    def write_inputs(self, inputs: dataclass):
        pass

    @abstractmethod
    def advance(self, dt: float):
        """Advance the model by dt global time units."""
        pass
