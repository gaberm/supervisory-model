from dataclasses import dataclass


@dataclass(frozen=True)
class ArrivedVehicle:
    vehicle_id: int
    soc_at_arrival: float
    building_id: int
    arrival_time: float


class DepartedVehicle:
    vehicle_id: int
    tour_id: int
    departure_time: float


@dataclass(frozen=True)
class TransportationOutputs:
    arrived_vehicles: tuple[ArrivedVehicle, ...]
    departed_vehicles: tuple[DepartedVehicle, ...]
