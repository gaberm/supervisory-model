from typing import Any
import psycopg2 as psycopg
from models.inputs.transportation import TransportationInputs, VehicleSoc
from supervisory.inputs.base import BaseLoader, BaseInputLoader


class VehicleSocLoader(BaseLoader[VehicleSoc]):
    def __init__(self, conn: psycopg.extensions.connection):
        self.conn = conn

    def _extract(self, timestep: float) -> list[tuple[Any, ...]]:
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT vehicle_id, soc, timestep
                FROM vehicle_soc
                WHERE timestep = %s
                """,
                (timestep,),
            )
            rows = cursor.fetchall()
        return rows

    def _build(self, rows: list[tuple[Any, ...]]) -> VehicleSoc:
        return (
            VehicleSoc(
                vehicle_id=row[0],
                soc=row[1],
                timestep=row[2],
            )
            for row in rows
        )


class TransportationInputLoader(BaseInputLoader):
    def __init__(self, conn: psycopg.extensions.connection):
        self.vehicle_soc_loader = VehicleSocLoader(conn)

    def load(self, timestep: float) -> TransportationInputs:
        return TransportationInputs(
            vehicles_soc=self.vehicle_soc_loader.load(timestep),
        )
