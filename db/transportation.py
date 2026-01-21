from db.table_schema import TableSchema

class ParkingTableSchema(TableSchema):
    def __init__(self):
        super().__init__(table_name="parking")

    def create_table_query(self) -> str:
        return """
        CREATE TABLE IF NOT EXISTS parking (
            vehicle_id INTEGER PRIMARY KEY,
            tour_id INTEGER,
            arr_time REAL,
            building_id TEXT,
            vehicle_type TEXT
        );
        """