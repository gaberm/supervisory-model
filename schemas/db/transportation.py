from .table_schema import TableSchema
from ...db.model_schema import ModelSchema


# class ParkingTable(TableSchema):
#     def name(self) -> str:
#         return "parking"

#     def create_sql(self) -> str:
#         return """
#         CREATE TABLE IF NOT EXISTS parking (
#             event_id SERIAL PRIMARY KEY,
#             vehicle_id INTEGER NOT NULL,
#             tour_id INTEGER NOT NULL,
#             building_id INTEGER NOT NULL,
#             arrival_time DOUBLE PRECISION NOT NULL,
#             end_time DOUBLE PRECISION,
#         );
#         """

#     def insert_statement(self) -> str:
#         return """
#         INSERT INTO parking (
#             vehicle_id,
#             tour_id,
#             building_id,
#             arrival_time
#         ) VALUES (%s, %s, %s, %s);
#         """


class ChargingTable(TableSchema):
    def name(self) -> str:
        return "charging"

    def create_sql(self) -> str:
        return """
        CREATE TABLE IF NOT EXISTS charging (
            vehicle_id INTEGER PRIMARY KEY,
            tour_id INTEGER NOT NULL,
            building_id INTEGER NOT NULL,
            soc_start DOUBLE PRECISION NOT NULL,
            soc_end DOUBLE PRECISION,
            start_time DOUBLE PRECISION NOT NULL,
            end_time DOUBLE PRECISION,
        );
        """


class TransportationSchema(ModelSchema):
    def tables(self) -> dict[str, TableSchema]:
        return {
            "charging": ChargingTable(),
        }
