from traitlets import Any
from adapters import ModelAdapter
from models.outputs import (
    DepartedVehicle,
    TransportationOutputs,
    ArrivedVehicle,
)
from models.inputs import TransportationInputs
import traci
import re
from adapters.helpers.sumo import EdgeToBuildingAssigner, TourIdLookup


class SumoAdapter(ModelAdapter):
    def __init__(
        self,
        name: str,
        timestep_length: int,
        sumo_config: str,
    ):
        super().__init__(name, timestep_length)
        self.sumo_config = sumo_config

        self._traci = None
        self._current_time = 0.0

    def current_time(self) -> float:
        return self._current_time

    def initialize(self):
        traci.start(["sumo", "-c", self.sumo_config])
        self._traci = traci
        self.timestep_length = traci.simulation.getDeltaT()

    def read_outputs(self) -> TransportationOutputs:
        return TransportationOutputs(
            departed_vehicles=self._get_departed_vehicles(),
            arrived_vehicles=self._get_arrived_vehicles(),
        )

    def _get_departed_vehicles(self) -> tuple[DepartedVehicle, ...]:
        return tuple(
            DepartedVehicle(
                vehicle_id=int(re.sub(r"^(person_|truck_)", "", vid)),
                departing_time=self._current_time,
            )
            for vid in traci.simulation.getDepartedIDList()
        )

    def _get_arrived_vehicles(self) -> tuple[ArrivedVehicle, ...]:
        return tuple(
            ArrivedVehicle(
                vehicle_id=int(re.sub(r"^(person_|truck_)", "", vid)),
                soc_at_arrival=traci.vehicle.getBatteryCapacity(vid),
                road_id=traci.vehicle.getRoadID(vid),
                arrival_time=self._current_time,
            )
            for vid in traci.simulation.getArrivedIDList()
        )

    def read_inputs(self, inputs: TransportationInputs):
        for vehicle_id, new_soc in inputs.vehicles_soc:
            self._set_vehicle_soc(str(vehicle_id), new_soc)

    def _set_vehicle_soc(self, vehicle_id: str, soc: float):
        traci.vehicle.setParameter(
            vehicle_id, "device.battery.actualBatteryCapacity", str(soc * 100)
        )

    def advance(self, dt: float):
        if dt % self.timestep_length != 0:
            raise ValueError(
                f"SUMO adapter cannot advance by dt={dt}. It must be a multiple of the timestep length {self.timestep_length}."
            )

        steps = int(dt / self.timestep_length)
        for _ in range(steps):
            self._traci.simulationStep()
            self._current_time += self.timestep_length
