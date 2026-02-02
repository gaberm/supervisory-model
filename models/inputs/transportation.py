from dataclasses import dataclass


@dataclass(frozen=True)
class VehicleSoc:
    vehicle_id: int
    soc: float


@dataclass(frozen=True)
class TransportationInputs:
    vehicles_soc: tuple[VehicleSoc, ...]
