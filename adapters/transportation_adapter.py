from adapters import BaseAdapter
from models.outputs import (
    DepartedVehicle,
    TransportationOutputs,
    ArrivedVehicle,
)
from models.inputs import TransportationInputs
import traci
import re


class TransportationAdapter(BaseAdapter):
    InputType = TransportationInputs
    OutputType = TransportationOutputs

    def __init__(self, config):
        super().__init__(
            name=config.model.transportation.name,
        )
        self._sumo_config = config.model.transportation.sumo_config
        self._traci = None

    def initialize(self):
        traci.start(["sumo", "-c", self._sumo_config])
        self._traci = traci
        self.timestep_length = self._traci.simulation.getDeltaT()

    def read_outputs(self) -> TransportationOutputs:
        return TransportationOutputs(
            departed_vehicles=self._get_departed_vehicles(),
            arrived_vehicles=self._get_arrived_vehicles(),
        )

    def _get_departed_vehicles(self) -> tuple[DepartedVehicle, ...]:
        return tuple(
            DepartedVehicle(
                vehicle_id=int(re.sub(r"^(person_|truck_)", "", vid)),
                departing_time=self.model_time,
            )
            for vid in self._traci.simulation.getDepartedIDList()
        )

    def _get_arrived_vehicles(self) -> tuple[ArrivedVehicle, ...]:
        return tuple(
            ArrivedVehicle(
                vehicle_id=int(re.sub(r"^(person_|truck_)", "", vid)),
                soc_at_arrival=self._traci.vehicle.getBatteryCapacity(vid),
                road_id=self._traci.vehicle.getRoadID(vid),
                arrival_time=self.model_time,
            )
            for vid in self._traci.simulation.getArrivedIDList()
        )

    def read_inputs(self, inputs: TransportationInputs):
        for vehicle_id, new_soc in inputs.vehicles_soc:
            self._set_vehicle_soc(str(vehicle_id), new_soc)

    def _set_vehicle_soc(self, vehicle_id: str, soc: float):
        self._traci.vehicle.setParameter(
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
            self._model_time += self.timestep_length

    def terminate(self):
        if self._traci is not None:
            self._traci.close()
            self._traci = None
