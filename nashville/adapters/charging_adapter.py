from adapter import Adapter
from nashville.entities.port import Port
from nashville.inputs.charging import ArrivedVehicles, DepartedVehicles
from nashville.models.charging_model import ChargingModel


class ChargingAdapter(Adapter):
    InputType = list[ArrivedVehicles, DepartedVehicles]
    OutputType = list[Port]

    @classmethod
    def from_config(cls, model_cfg) -> "ChargingAdapter":
        return cls(
            name=model_cfg.name,
            timestep_length=model_cfg.timestep_length,
            charging_rate=model_cfg.charging_rate,
        )

    def __init__(self, name, timestep_length, charging_rate):
        super().__init__(
            name=name,
            timestep_length=timestep_length,
        )
        self._charging_rate = charging_rate
        self._charging_model = None

        self._charged_vehicles = None

    def initialize(self):
        self._charging_model = ChargingModel(charging_rate=self._charging_rate)

    def read_outputs(self) -> list[Port]:
        return [
            Port(
                port_id=vehicle_id,
                station_id="default_station",  # Replace with actual station ID if available
                power_usage=self._charging_rate,
                status="charging",
                time=self.model_time,
            )
            for vehicle_id in self._charging_model.get_charging_vehicles()
        ]

    def _get_charging_vehicles(self) -> tuple[ChargingVehicleRecord, ...]:
        outputs = self._charging_model.get_all_soc()
        return tuple(
            ChargingVehicleRecord(
                vehicle_id=vehicle_id,
                soc=soc,
                timestamp=self.model_time,
            )
            for vehicle_id, soc in outputs.items()
        )

    def write_inputs(self, inputs: ChargingInputs):
        for vehicle in inputs.vehicles_to_add:
            self._charging_model.add_vehicle(
                vehicle.vehicle_id, initial_soc=vehicle.initial_soc
            )
        self._save_charged_vehicles(inputs)
        for vehicle in inputs.vehicles_to_remove:
            self._charging_model.remove_vehicle(vehicle.vehicle_id)

    def _save_charged_vehicles(self, inputs: ChargingInputs):
        self._charged_vehicles = tuple(
            ChargedVehicleRecord(
                vehicle_id=vehicle.vehicle_id,
                soc=self._charging_model.get_soc(vehicle.vehicle_id),
                ended_at=self.model_time,
            )
            for vehicle in inputs.vehicles_to_remove
        )

    def advance(self, dt: float):
        if dt % self.timestep_length != 0:
            raise ValueError(
                f"SUMO adapter cannot advance by dt={dt}. It must be a multiple of the timestep length {self.timestep_length}."
            )

        steps = int(dt / self.timestep_length)
        for _ in range(steps):
            self._charging_model.charge()
            self._model_time += self.timestep_length

    def terminate(self):
        self._charging_model = None
