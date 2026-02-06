from dataclasses import dataclass
from typing import Dict, List, Type
import psycopg
from adapters import BaseAdapter, ChargingAdapter, TransportationAdapter
from state_memory import StateMemory
from supervisory.loaders.base_loader import BaseInputLoader
from supervisory.loaders import ChargingInputLoader, TransportationInputLoader

ADAPTERS: Dict[str, Type[BaseAdapter]] = {
    "charging": ChargingAdapter,
    "transportation": TransportationAdapter,
}

INPUTS_LOADERS: Dict[Type, Type[BaseInputLoader]] = {
    "charging": ChargingInputLoader,
    "transportation": TransportationInputLoader,
}


class SupervisoryModel:
    def __init__(self, config):
        self.adapters = self._create_adapters(config)
        self.state_memory = StateMemory(config.db.url)
        self._create_tables()

        self.global_time = 0.0
        self.global_timestep_length = self._global_timestep_length()

        self.lagging_adapter_names: List[str] = []

    def _create_adapters(self, config) -> Dict[str, BaseAdapter]:
        adapters = {}
        for key, AdapterClass in ADAPTERS.items():
            value = getattr(config.model, key, None)
            if value is not None:
                adapters[key] = AdapterClass(value)
        return adapters

    def _global_timestep_length(self) -> float:
        return min(adapter.timestep_length for adapter in self.adapters.values())

    def initialize_adapters(self):
        for adapter in self.adapters.values():
            adapter.initialize()

    def _create_tables(self):
        for adapter in self.adapters.values():
            if adapter.OutputType is not None:
                self.state_memory.create_output_table(adapter.OutputType)
            else:
                raise ValueError(
                    f"Adapter {adapter.name} does not have an OutputType defined."
                )

    def write_inputs(self):
        for adapter_name in self.lagging_adapter_names:
            inputs = INPUTS_LOADERS[adapter_name].load_input(
                self.state_memory.conn, self.global_time
            )
            self.adapters[adapter_name].write_inputs(inputs)

    def advance_components(self, dt: float):
        for adapter in self.adapters.values():
            adapter.advance(dt)
        self.global_time += dt

    def read_outputs(self):
        for adapter_name in self.lagging_adapter_names:
            output = self.adapters[adapter_name].read_outputs()
            self.state_memory.insert_output(output)

    def find_lagging_adapters(self):
        min_model_time = min(adapter.model_time for adapter in self.adapters.values())
        self.lagging_adapter_names = [
            name
            for name, adapter in self.adapters.items()
            if adapter.model_time == min_model_time
        ]

    def terminate(self):
        for adapter in self.adapters.values():
            adapter.terminate()
        self.state_memory.close()
