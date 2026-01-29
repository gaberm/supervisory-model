from dataclasses import dataclass


@dataclass(frozen=True)
class DepartingVehicle:
    vehicle_id: int
    tour_id: int
    departing_time: float


@dataclass(frozen=True)
class ArrivingVehicle:
    vehicle_id: int
    tour_id: int
    arrival_time: float
    arrival_building_id: int
    soc: float


@dataclass(frozen=True)
class SumoOutputs:
    departing_vehicles: tuple[DepartingVehicle, ...]
    arriving_vehicles: tuple[ArrivingVehicle, ...]
