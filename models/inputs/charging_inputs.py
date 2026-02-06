from dataclasses import dataclass


@dataclass(frozen=True)
class VehicleToAdd:
    vehicle_id: int
    initial_soc: float


@dataclass(frozen=True)
class VehicleToRemove:
    vehicle_id: int


@dataclass(frozen=True)
class ChargingInputs:
    vehicles_to_add: tuple[VehicleToAdd, ...]
    vehicles_to_remove: tuple[VehicleToRemove, ...]
