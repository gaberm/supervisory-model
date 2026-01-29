from traitlets import Any
from adapters import ModelAdapter
from ..models.charging import ChargingModel
from ..schemas.adapters.charging import ChargingOutputs, ChargingInputs, Soc


class ChargingAdapter(ModelAdapter):
    def __init__(
        self,
        name: str,
        timestep_length: float,
        charging_rate: float,
    ):
        super().__init__(name, timestep_length)
        self.charging_rate = charging_rate
        self.charging_model = None

    def initialize(self):
        self.charging_model = ChargingModel(
            strategy=self.strategy, charging_rate=self.charging_rate
        )

    def read_outputs(self) -> ChargingOutputs:
        # Read outputs from the charging simulation
        outputs = self.charging_model.get_all_soc()
        outputs = ChargingOutputs(
            vehicles_soc=tuple(
                Soc(vehicle_id=vid, soc=soc) for vid, soc in outputs.items()
            )
        )
        return outputs

    def write_inputs(self, inputs: ChargingInputs):
        for vehicle in inputs.vehicles_to_add:
            self.charging_model.add_vehicle(
                vehicle.vehicle_id, initial_soc=vehicle.initial_soc
            )
        for vehicle_id in inputs.vehicles_to_remove:
            self.charging_model.remove_vehicle(vehicle_id)

    def advance(self, dt: float):
        if dt % self.timestep_length != 0:
            raise ValueError(
                f"SUMO adapter cannot advance by dt={dt}. It must be a multiple of the timestep length {self.timestep_length}."
            )

        steps = int(dt / self.timestep_length)
        for _ in range(steps):
            self.charging_model.charge()
            self.current_time += self.timestep_length
