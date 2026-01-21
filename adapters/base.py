from abc import ABC, abstractmethod

class ModelAdapter(ABC):
    def __init__(self, name: str, timestep: int):
        self.name = name
        self.timestep = timestep
        self.current_time = 0.0

    @abstractmethod
    def read_outputs(self) -> dict:
        pass

    @abstractmethod
    def write_inputs(self, inputs: dict):
        pass

    @abstractmethod
    def advance(self, dt: float):
        pass