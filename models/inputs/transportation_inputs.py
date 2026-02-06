from dataclasses import dataclass


@dataclass(frozen=True)
class VehicleSoc:
    vehicle_id: int
    soc: float
    stop_time: float


@dataclass(frozen=True)
class TransportationInputs:
    vehicles_soc: tuple[VehicleSoc, ...]
