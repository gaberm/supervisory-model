from dataclasses import dataclass
from models.outputs.decorator import record


@record(
    table="arrived_vehicles",
    key=("vehicle_id",),
)
@dataclass(frozen=True)
class ArrivedVehicle:
    vehicle_id: int
    soc_at_arrival: float
    road_id: int
    arrival_time: float


@record(
    table="departed_vehicles",
    key=("vehicle_id",),
)
@dataclass(frozen=True)
class DepartedVehicle:
    vehicle_id: int
    departure_time: float


@dataclass(frozen=True)
class TransportationOutputs:
    arrived_vehicles: tuple[ArrivedVehicle, ...]
    departed_vehicles: tuple[DepartedVehicle, ...]
