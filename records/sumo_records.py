from dataclasses import dataclass
from typing import ClassVar, Optional
from records.base_record import BaseRecord


@dataclass(frozen=True, kw_only=True)
class ArrivedVehicleRecord(BaseRecord):
    table_name: ClassVar[str] = "arrived_vehicles"
    primary_key: ClassVar[tuple[str, ...]] = ("vehicle_id", "global_time")
    indexed: ClassVar[tuple[str, ...]] = ("global_time",)
    domain: ClassVar[Optional[str]] = "transport"

    vehicle_id: str
    road_id: str
    soc_at_arrival: float


@dataclass(frozen=True, kw_only=True)
class DepartedVehicleRecord(BaseRecord):
    table_name: ClassVar[str] = "departed_vehicles"
    primary_key: ClassVar[tuple[str, ...]] = ("vehicle_id", "global_time")
    domain: ClassVar[Optional[str]] = "transport"

    vehicle_id: str
    road_id: str


@dataclass(frozen=True, kw_only=True)
class VehicleStateRecord(BaseRecord):
    table_name: ClassVar[str] = "vehicle_state"
    primary_key: ClassVar[tuple[str, ...]] = ("vehicle_id", "global_time")
    indexed: ClassVar[tuple[str, ...]] = ("global_time",)
    domain: ClassVar[Optional[str]] = "transport"

    vehicle_id: str
    road_id: str
    speed: float
