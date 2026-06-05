from adapter import Adapter
from ..entities.vehicle import Vehicle
from ..inputs.sumo import VehicleSocInput
import traci
from traci.constants import VAR_ROAD_ID


class SumoAdapter(Adapter):
    InputType = VehicleSocInput
    OutputType = Vehicle

    def __init__(self, name, timestep_length, sumo_config):
        super().__init__(
            name=name,
            timestep_length=timestep_length,
        )
        self._sumo_config = sumo_config
        self._traci = None

    def initialize(self):
        traci.start(["sumo", "-c", self._sumo_config])
        self._traci = traci
        self._timestep_length = self._traci.simulation.getDeltaT()

    def read_outputs(self) -> list[Vehicle]:
        output = []
        output += self._get_arrived_vehicles()
        output += self._get_departed_vehicles()
        return output

    def _get_vehicle_coord(self, v_id: str) -> tuple[float, float]:
        return self._traci.simulation.convertGeo(*self._traci.vehicle.getPosition(v_id))

    def _get_vehicle_soc(self, v_id: str) -> float:
        try:
            soc = self._traci.vehicle.getParameter(
                v_id, "device.battery.actualBatteryCapacity"
            )
            return float(soc) / 100
        except traci.exceptions.TraCIException:
            return None

    def _get_arrived_vehicles(self) -> list[Vehicle]:
        return [
            Vehicle(
                veh_id=veh_id,
                soc=self._get_vehicle_soc(veh_id),
                state="arrived",
                time=self.model_time,
                lon=self._get_vehicle_coord(veh_id)[0],
                lat=self._get_vehicle_coord(veh_id)[1],
            )
            for veh_id in self._traci.simulation.getArrivedIDList()
        ]

    def _get_departed_vehicles(self) -> list[Vehicle]:
        return [
            Vehicle(
                veh_id=v_id,
                soc=self._get_vehicle_soc(v_id),
                state="departed",
                time=self.model_time,
                lon=self._get_vehicle_coord(v_id)[0],
                lat=self._get_vehicle_coord(v_id)[1],
            )
            for v_id in self._traci.simulation.getDepartedIDList()
        ]

    def write_inputs(self, inputs: list[dict]):
        for item in inputs:
            self._set_vehicle_soc(str(item["veh_id"]), item["soc"])

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
