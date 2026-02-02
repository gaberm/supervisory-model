from dataclasses import dataclass
from typing import Any
import psycopg


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


class ChargingInputConstructor:
    def read_tables(self, conn: psycopg.Connection, time) -> dict[str, Any]:
        table_data = {}
        table_data["vehicles_to_add"] = conn.execute(
            "SELECT vehicle_id, soc_at_departure FROM arriving_vehicles WHERE arrival_time <= %s;",
            (time,),
        ).fetchall()
        table_data["vehicles_to_remove"] = conn.execute(
            "SELECT vehicle_id FROM departing_vehicles WHERE departure_time <= %s;",
            (time,),
        ).fetchall()
        return table_data

    def build_inputs(self, table_data: dict[str, Any]) -> ChargingInputs:
        vehicles_to_add = tuple(
            VehicleToAdd(vehicle_id=row[0], initial_soc=row[1])
            for row in table_data["vehicles_to_add"]
        )
        vehicles_to_remove = tuple(
            VehicleToRemove(vehicle_id=row[0])
            for row in table_data["vehicles_to_remove"]
        )
        return ChargingInputs(
            vehicles_to_add=vehicles_to_add, vehicles_to_remove=vehicles_to_remove
        )
