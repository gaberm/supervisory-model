from traitlets import Any
from adapters import BaseAdapter
from ..models.charging_model import ChargingModel
from models.outputs import ChargingOutputs, VehicleSoc
from models.inputs import ChargingInputs


class ChargingAdapter(BaseAdapter):
    InputType = ChargingInputs
    OutputType = ChargingOutputs

    def __init__(self, config):
        super().__init__(
            name=config.model.transportation.name,
            timestep_length=config.model.transportation.timestep_length,
        )
        self._charging_rate = config.model.transportation.charging_rate
        self._charging_model = None

    def initialize(self):
        self._charging_model = ChargingModel(charging_rate=self._charging_rate)

    def read_outputs(self) -> ChargingOutputs:
        # Read outputs from the charging simulation
        outputs = self._charging_model.get_all_soc()
        outputs = ChargingOutputs(
            vehicles_soc=tuple(
                VehicleSoc(vehicle_id=vid, soc=soc, stop_time=self.model_time)
                for vid, soc in outputs.items()
            )
        )
        return outputs

    def write_inputs(self, inputs: ChargingInputs):
        for vehicle in inputs.vehicles_to_add:
            self._charging_model.add_vehicle(
                vehicle.vehicle_id, initial_soc=vehicle.initial_soc
            )
        for vehicle_id in inputs.vehicles_to_remove:
            self._charging_model.remove_vehicle(vehicle_id)

    def advance(self, dt: float):
        if dt % self.timestep_length != 0:
            raise ValueError(
                f"SUMO adapter cannot advance by dt={dt}. It must be a multiple of the timestep length {self.timestep_length}."
            )

        steps = int(dt / self.timestep_length)
        for _ in range(steps):
            self._charging_model.charge()
            self.model_time += self.timestep_length
