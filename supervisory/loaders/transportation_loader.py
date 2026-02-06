from typing import Any
import psycopg2 as psycopg
from models.inputs.transportation_inputs import TransportationInputs, VehicleSoc
from supervisory.loaders.base_loader import BaseLoader, BaseInputLoader


class VehicleSocLoader(BaseLoader[VehicleSoc]):
    def _extract(
        self, conn: psycopg.extensions.connection, time: float
    ) -> list[tuple[Any, ...]]:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT vehicle_id, soc, stop_time
                FROM vehicle_soc
                WHERE stop_time = %s
                """,
                (time,),
            )
            rows = cursor.fetchall()
        return rows

    def _build(self, rows: list[tuple[Any, ...]]) -> VehicleSoc:
        return (
            VehicleSoc(
                vehicle_id=row[0],
                soc=row[1],
                stop_time=row[2],
            )
            for row in rows
        )


class TransportationInputLoader(BaseInputLoader):
    def load_input(
        self, conn: psycopg.extensions.connection, time: float
    ) -> TransportationInputs:
        return TransportationInputs(
            vehicles_soc=VehicleSocLoader().load_input(conn, time),
        )
