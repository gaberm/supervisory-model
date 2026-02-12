from typing import Any
import psycopg2 as psycopg
from models.inputs.transportation_inputs import TransportationInputs, VehicleSoc
from supervisory.loaders.base_loader import BaseLoader, BaseInputLoader
from supervisory.time import TimeRange


class VehicleSocLoader(BaseLoader[VehicleSoc]):
    @staticmethod
    def _extract(
        conn: psycopg.extensions.connection, time_range: TimeRange
    ) -> list[tuple[Any, ...]]:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT vehicle_id, soc, ended_at
                FROM charged_vehicles
                WHERE ended_at >= %s AND ended_at < %s
                """,
                (time_range.start_time, time_range.end_time),
            )
            rows = cursor.fetchall()
        return rows

    @staticmethod
    def _transform(
        rows: list[tuple[Any, ...]], time_range: TimeRange, charge_rate: float
    ) -> list[tuple[Any, ...]]:
        return [
            tuple(
                row[0],
                row[1] + (time_range.end_time - row[2]) * charge_rate,
                time_range.end_time,
            )
            for row in rows
        ]

    @staticmethod
    def _build(rows: list[tuple[Any, ...]]) -> VehicleSoc:
        return (
            VehicleSoc(
                vehicle_id=row[0],
                soc=row[1],
                stop_time=row[2],
            )
            for row in rows
        )

    @staticmethod
    def load_input(
        conn: psycopg.extensions.connection, time_range: TimeRange, charge_rate: float
    ) -> VehicleSoc:
        rows = VehicleSocLoader._extract(conn, time_range)
        rows = VehicleSocLoader._transform(rows, time_range, charge_rate)
        return VehicleSocLoader._build(rows)


class TransportationInputLoader(BaseInputLoader):
    def __init__(self, charge_rate: float):
        self.charge_rate = charge_rate

    @classmethod
    def from_config(cls, config):
        return cls(charge_rate=config.models.charging.charging_rate)

    def load_input(
        self, conn: psycopg.extensions.connection, time_range: TimeRange
    ) -> TransportationInputs:
        return TransportationInputs(
            vehicles_soc=VehicleSocLoader.load_input(
                conn, time_range, self.charge_rate
            ),
        )
