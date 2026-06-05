from abc import ABC, abstractmethod
from typing import Mapping
from base.entity import Entity
from base.input import Input


class Adapter(ABC):
    InputType: type[Input] | list[type[Input]]
    OutputType: type[Entity] | list[type[Entity]]

    def __init__(self, name: str, timestep_length: float, **kwargs):
        self.name = name
        self._timestep_length = timestep_length
        self._model_time = 0.0

    @property
    def model_time(self) -> float:
        """Return the model's current simulation time in global time units."""
        return self._model_time

    @property
    def timestep_length(self) -> float:
        """Return the model's timestep length in global time units."""
        return self._timestep_length

    @abstractmethod
    def initialize(self):
        """Initialize the model."""
        pass

    @abstractmethod
    def read_outputs(self) -> list[Entity]:
        """Read the user-defined outputs of the model."""
        pass

    @abstractmethod
    def write_inputs(self, inputs: Mapping[type[Input], list]):
        """Write user-defined inputs to the model."""
        pass

    @abstractmethod
    def advance(self, dt: float):
        """Advance the model by dt global time units."""
        pass

    @abstractmethod
    def terminate(self):
        """Terminate the model."""
        pass
