import dataclasses
import psycopg2 as psycopg
from .type_mapping import sql_type


class StateMemory:
    def __init__(self, db_url: str):
        self.conn = psycopg.connect(db_url)

    def reset_tables(self, drop_tables: bool = False):
        with self.conn.cursor() as cur:
            if drop_tables:
                cur.execute(
                    """
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                    """
                )
                tables = cur.fetchall()
                for (table_name,) in tables:
                    cur.execute(f"DROP TABLE IF EXISTS {table_name} CASCADE")
            self.conn.commit()

    def create_output_tables(self, cls):
        for sql in self._generate_create_table_sql(cls):
            with self.conn.cursor() as cur:
                cur.execute(sql)
            self.conn.commit()

    def _generate_create_table_sql(self, cls) -> list[str]:
        output_classes = self._extract_output_classes(cls)
        return [self._table_sql(output_cls) for output_cls in output_classes]

    def _extract_output_classes(self, cls):
        """Recursively extract all dataclasses that are decorated with @record."""
        output_classes = set()

        for field in dataclasses.fields(cls):
            field_type = field.type
            if hasattr(field_type, "__origin__"):  # Generic type
                args = getattr(field_type, "__args__", ())
                for arg in args:
                    if dataclasses.is_dataclass(arg) and hasattr(arg, "__record__"):
                        output_classes.add(arg)
                        output_classes.update(self._extract_output_classes(arg))

        return output_classes

    def _column_sql(self, cls) -> list[str]:
        return [
            f"{field.name} {sql_type(field.type)}" for field in dataclasses.fields(cls)
        ]

    def _primary_key_sql(self, cls) -> str:
        key = cls.__record__["key"]
        return f", PRIMARY KEY ({', '.join(key)})" if key else ""

    def _table_sql(self, cls) -> str:
        table = cls.__record__["table"]
        return f"""
                CREATE TABLE IF NOT EXISTS {table} (
                    {', '.join(self._column_sql(cls))}
                    {self._primary_key_sql(cls)}
                );
        """.strip()

    def insert_output(self, output):
        for field in dataclasses.fields(output):
            value = getattr(output, field.name)
            if not value:
                continue
            if isinstance(value, tuple):
                for record in value:
                    self._insert_record(record)
            elif dataclasses.is_dataclass(value):
                self._insert_record(value)

    def _insert_record(self, record):
        record_cls = type(record)
        if not hasattr(record_cls, "__record__"):
            raise ValueError(
                f"Record {record_cls.__name__} is missing __record__ metadata."
            )
        sql = self._generate_insert_sql(record_cls)
        values = self._extract_values(record)
        with self.conn.cursor() as cur:
            cur.execute(sql, values)
        self.conn.commit()

    def _extract_values(self, record) -> list:
        return [getattr(record, field.name) for field in dataclasses.fields(record)]

    def _generate_insert_sql(self, cls) -> str:
        table = cls.__record__["table"]
        fields = [field.name for field in dataclasses.fields(cls)]
        placeholders = ", ".join(["%s"] * len(fields))
        sql = f"INSERT INTO {table} ({', '.join(fields)}) VALUES ({placeholders})"
        return sql

    def close_conn(self):
        self.conn.close()
