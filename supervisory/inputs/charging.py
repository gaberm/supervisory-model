from typing import Any
import psycopg2 as psycopg
from models.inputs import ChargingInputs, VehicleToAdd, VehicleToRemove
from supervisory.inputs.base import BaseLoader, BaseInputLoader


class VehicleToAddLoader(BaseLoader[VehicleToAdd]):
    def __init__(self, conn: psycopg.extensions.connection):
        self.conn = conn

    def _extract(self, arrival_time) -> list[VehicleToAdd]:
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT vehicle_id, soc_at_departure
                FROM arriving_vehicles
                WHERE arrival_time <= %s
                """,
                (arrival_time,),
            )
            rows = cursor.fetchall()
        return rows

    def _build(self, rows: list[tuple[Any, ...]]) -> VehicleToAdd:
        return (
            VehicleToAdd(
                vehicle_id=row[0],
                initial_soc=row[1],
            )
            for row in rows
        )


class VehicleToRemoveLoader(BaseLoader[VehicleToRemove]):
    def __init__(self, conn: psycopg.extensions.connection):
        self.conn = conn

    def _extract(self, departure_time) -> list[tuple[Any, ...]]:
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT vehicle_id
                FROM departing_vehicles
                WHERE departure_time <= %s
                """,
                (departure_time,),
            )
            rows = cursor.fetchall()
        return rows

    def _build(self, rows: list[tuple[Any, ...]]) -> VehicleToRemove:
        return (
            VehicleToRemove(
                vehicle_id=row[0],
            )
            for row in rows
        )


class ChargingInputConstructor(BaseInputLoader):
    def __init__(self, conn: psycopg.extensions.connection):
        self.vehicle_to_add_loader = VehicleToAddLoader(conn)
        self.vehicle_to_remove_loader = VehicleToRemoveLoader(conn)

    def load(self, time) -> ChargingInputs:
        return ChargingInputs(
            vehicles_to_add=tuple(self.vehicle_to_add_loader.load(time)),
            vehicles_to_remove=tuple(self.vehicle_to_remove_loader.load(time)),
        )
