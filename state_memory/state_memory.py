import dataclasses
import psycopg2 as psycopg
from type_mapping import sql_type


class StateMemory:
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.conn = None

    def connect(self):
        self.conn = psycopg.connect(self.db_url)

    def create_output_table(self, cls):
        sql = self._generate_create_table_sql(cls)

        with self.conn.cursor() as cur:
            cur.execute(sql)
        self.conn.commit()

    def _generate_create_table_sql(self, cls) -> str:
        meta = cls.__record__
        table = meta["table"]
        key = meta["key"]

        columns = [
            f"{field.name} {sql_type(field.type)}" for field in dataclasses.fields(cls)
        ]

        pk = f", PRIMARY KEY ({', '.join(key)})" if key else ""

        return f"""
        CREATE TABLE IF NOT EXISTS {table} (
            {', '.join(columns)}
            {pk}
        );
        """.strip()

    def insert_output(self, obj):
        sql, values = self._generate_insert_sql(obj)

        with self.conn.cursor() as cur:
            cur.execute(sql, values)
        self.conn.commit()

    def _generate_insert_sql(self, obj):
        cls = obj.__class__
        meta = cls.__record__
        table = meta["table"]

        fields = [field.name for field in dataclasses.fields(cls)]
        values = [getattr(obj, field) for field in fields]

        placeholders = ", ".join(["%s"] * len(fields))
        sql = f"INSERT INTO {table} ({', '.join(fields)}) VALUES ({placeholders})"

        return sql, values
