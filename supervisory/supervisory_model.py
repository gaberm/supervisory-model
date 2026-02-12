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
from tqdm import tqdm

logger = logging.getLogger(__name__)

ADAPTERS: Dict[str, Type[BaseAdapter]] = {
    "charging": ChargingAdapter,
    "transportation": TransportationAdapter,
}

INPUTS_LOADERS: Dict[str, Type[BaseInputLoader]] = {
    "charging": ChargingInputLoader,
    "transportation": TransportationInputLoader,
}


class SupervisoryModel:
    def __init__(self, config):
        self.adapters = self._create_adapters(config)
        self.input_loaders = self._create_input_loaders(config)
        self.state_memory = StateMemory(config.db.db_url)
        self.max_global_time = config.simulation.max_global_time

        self.lagging_adapter_names: List[str] = []
        self._min_model_time = 0.0

    def _create_adapters(self, config) -> Dict[str, BaseAdapter]:
        adapters = {}
        for key, AdapterClass in ADAPTERS.items():
            value = config.models.get(key)
            if value is not None:
                adapters[key] = AdapterClass(config)
        return adapters

    def _create_input_loaders(self, config) -> Dict[str, BaseInputLoader]:
        input_loaders = {}
        for adapter_name in self.adapters.keys():
            loader_class = INPUTS_LOADERS.get(adapter_name)
            if loader_class is None:
                raise ValueError(
                    f"No input loader configured for adapter '{adapter_name}'."
                )
            if hasattr(loader_class, "from_config"):
                input_loaders[adapter_name] = loader_class.from_config(config)
            else:
                input_loaders[adapter_name] = loader_class()
        return input_loaders

    def reset_state_memory(self, drop_tables: bool = False):
        logger.info("Resetting state memory tables.")
        self.state_memory.reset_tables(drop_tables=drop_tables)

    def initialize_adapters(self):
        for adapter in self.adapters.values():
            adapter.initialize()

    def _create_tables(self):
        for adapter in self.adapters.values():
            if adapter.OutputType is not None:
                self.state_memory.create_output_tables(adapter.OutputType)
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
            inputs = self.input_loaders[adapter_name].load_input(
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
        self._min_model_time = min(
            adapter.model_time for adapter in self.adapters.values()
        )

    def run(self):
        logger.info("Starting simulation run.")
        self._create_tables()
        self.initialize_adapters()
        self.find_lagging_adapters()
        with tqdm(total=self.max_global_time, desc="Simulation Progress") as pbar:
            while self.lagging_adapter_names:
                self.write_inputs()
                self.advance_components()
                self.read_outputs()
                self.find_lagging_adapters()
                pbar.update(self._min_model_time - pbar.n)
        self._print_final_state()
        self.terminate()

    def _print_final_state(self):
        for adapter_name in self.adapters.keys():
            logger.info(
                f"Final model time for adapter '{adapter_name}': {self.adapters[adapter_name].model_time}"
            )

    def terminate(self):
        for adapter in self.adapters.values():
            adapter.terminate()
        self.state_memory.close_conn()
        logger.info("Simulation run completed.")
