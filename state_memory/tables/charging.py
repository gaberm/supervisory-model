from dataclasses import dataclass
from traitlets import Any
from ..schemas import TableSchema
from ..schemas import ModelSchema


class DepartingVehicleSoc(TableSchema):
    def name(self) -> str:
        return "departing_vehicles_soc"

    def create_sql(self) -> str:
        return """
        CREATE TABLE IF NOT EXISTS departing_vehicles_soc (
            vehicle_id INTEGER PRIMARY KEY,
            tour_id INTEGER NOT NULL,
            soc_at_departure DOUBLE PRECISION NOT NULL,
            departure_time DOUBLE PRECISION NOT NULL,
        );
        """

    def insert_sql(self) -> str:
        return """
        INSERT INTO departing_vehicles_soc (
            vehicle_id,
            tour_id,
            soc_at_departure,
            departure_time
        ) VALUES (%s, %s, %s, %s);
        """


class ChargingSchema(ModelSchema):
    def tables(self) -> dict[str, TableSchema]:
        return {
            "departing_vehicles_soc": DepartingVehicleSoc(),
        }
