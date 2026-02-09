from typing import Dict, List, Type
from adapters import BaseAdapter, ChargingAdapter, TransportationAdapter
from state_memory import StateMemory
from supervisory.loaders import (
    BaseInputLoader,
    ChargingInputLoader,
    TransportationInputLoader,
)
from supervisory.time import TimeRange
import logging

logger = logging.getLogger(__name__)

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
        self.max_global_time = config.model.max_global_time

        self.lagging_adapter_names: List[str] = []

    def _create_adapters(self, config) -> Dict[str, BaseAdapter]:
        adapters = {}
        for key, AdapterClass in ADAPTERS.items():
            value = getattr(config.model, key, None)
            if value is not None:
                adapters[key] = AdapterClass(value)
        return adapters

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
            time_interval = TimeRange(
                start_time=self.adapters[adapter_name].model_time,
                end_time=self.adapters[adapter_name].model_time
                + self.adapters[adapter_name].timestep_length,
            )
            inputs = INPUTS_LOADERS[adapter_name].load_input(
                self.state_memory.conn, time_interval
            )
            self.adapters[adapter_name].write_inputs(inputs)

    def advance_components(self):
        for adapter_name in self.lagging_adapter_names:
            self.adapters[adapter_name].advance(
                self.adapters[adapter_name].timestep_length
            )

    def read_outputs(self):
        for adapter_name in self.lagging_adapter_names:
            output = self.adapters[adapter_name].read_outputs()
            self.state_memory.insert_output(output)

    def find_lagging_adapters(self):
        next_step_time = min(
            adapter.model_time + adapter.timestep_length
            for adapter in self.adapters.values()
        )
        self.lagging_adapter_names = [
            name
            for name, adapter in self.adapters.items()
            if adapter.model_time + adapter.timestep_length
            == next_step_time
            <= self.max_global_time
        ]

    def run(self):
        logger.info("Starting simulation run.")
        self.initialize_adapters()
        self.find_lagging_adapters()
        while self.lagging_adapter_names:
            self.write_inputs()
            self.advance_components()
            self.read_outputs()
            self.find_lagging_adapters()
        self.terminate()

    def terminate(self):
        for adapter in self.adapters.values():
            adapter.terminate()
        self.state_memory.close()
        logger.info("Simulation run completed.")
