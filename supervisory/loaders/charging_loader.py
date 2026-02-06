from typing import Any
import psycopg2 as psycopg
from models.inputs import ChargingInputs, VehicleToAdd, VehicleToRemove
from supervisory.loaders.base_loader import BaseLoader, BaseInputLoader


class VehicleToAddLoader(BaseLoader[VehicleToAdd]):
    def _extract(
        self, conn: psycopg.extensions.connection, time: float
    ) -> list[VehicleToAdd]:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT vehicle_id, soc_at_departure
                FROM arriving_vehicles
                WHERE arrival_time <= %s
                """,
                (time,),
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
    def _extract(
        self, conn: psycopg.extensions.connection, time: float
    ) -> list[tuple[Any, ...]]:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT vehicle_id
                FROM departing_vehicles
                WHERE departure_time <= %s
                """,
                (time,),
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


class ChargingInputLoader(BaseInputLoader):
    def load_input(
        self, conn: psycopg.extensions.connection, time: float
    ) -> ChargingInputs:
        return ChargingInputs(
            vehicles_to_add=tuple(self.vehicle_to_add_loader.load(conn, time)),
            vehicles_to_remove=tuple(self.vehicle_to_remove_loader.load(conn, time)),
        )
