from dataclasses import dataclass
from typing import Any
from ..schemas import TableSchema
from ..schemas import ModelSchema


class ArrivingVehicleTable(TableSchema):
    def name(self) -> str:
        return "arriving_vehicles"

    def create_sql(self) -> str:
        return """
        CREATE TABLE IF NOT EXISTS arriving_vehicles (
            vehicle_id INTEGER PRIMARY KEY,
            tour_id INTEGER NOT NULL,
            building_id INTEGER NOT NULL,
            soc_at_arrival DOUBLE PRECISION NOT NULL,
            arrival_time DOUBLE PRECISION NOT NULL,
        );
        """

    def insert_sql(self) -> str:
        return """
        INSERT INTO arriving_vehicles (
            vehicle_id,
            tour_id,
            building_id,
            soc_at_arrival,
            arrival_time
        ) VALUES (%s, %s, %s, %s, %s);
        """


class DepartingVehicleTable(TableSchema):
    def name(self) -> str:
        return "departing_vehicles"

    def create_sql(self) -> str:
        return """
        CREATE TABLE IF NOT EXISTS departing_vehicles (
            vehicle_id INTEGER PRIMARY KEY,
            tour_id INTEGER NOT NULL,
            departure_time DOUBLE PRECISION NOT NULL,
        );
        """

    def insert_sql(self) -> str:
        return """
        INSERT INTO departing_vehicles (
            vehicle_id,
            tour_id,
            departure_time
        ) VALUES (%s, %s, %s);
        """


class TransportationSchema(ModelSchema):
    def tables(self) -> dict[str, TableSchema]:
        return {
            "arriving_vehicles": ArrivingVehicleTable(),
            "departing_vehicles": DepartingVehicleTable(),
        }
