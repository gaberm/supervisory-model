from dataclasses import dataclass
from typing import ClassVar
from records.base_record import BaseRecord


@dataclass(frozen=True, kw_only=True)
class ChargingVehicleRecord(BaseRecord):
    table_name: ClassVar[str] = "charging_vehicles"
    primary_key: ClassVar[tuple[str, ...]] = ("vehicle_id", "global_time")
    indexed: ClassVar[tuple[str, ...]] = ("global_time",)
    diagnostic: ClassVar[bool] = False

    vehicle_id: int
    soc: float


@dataclass(frozen=True, kw_only=True)
class ChargedVehicleRecord(BaseRecord):
    table_name: ClassVar[str] = "charged_vehicles"
    primary_key: ClassVar[tuple[str, ...]] = ("vehicle_id",)
    indexed: ClassVar[tuple[str, ...]] = ("global_time",)
    diagnostic: ClassVar[bool] = False

    vehicle_id: int
    soc: float
