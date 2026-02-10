import dataclasses
import psycopg2 as psycopg
from .type_mapping import sql_type


class StateMemory:
    def __init__(self, db_url: str):
        self.conn = psycopg.connect(db_url)

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

    def insert_output(self, cls):
        output_cls = self._extract_output_classes(cls)
        for cls in output_cls:
            sql = self._generate_insert_sql(cls)
            values = self._extract_values(cls)
            with self.conn.cursor() as cur:
                cur.execute(sql, values)
            self.conn.commit()

    def _extract_values(self, cls) -> list:
        return [getattr(cls, field.name) for field in dataclasses.fields(cls)]

    def _generate_insert_sql(self, cls) -> str:
        table = cls.__record__["table"]
        fields = [field.name for field in dataclasses.fields(cls)]
        placeholders = ", ".join(["%s"] * len(fields))
        sql = f"INSERT INTO {table} ({', '.join(fields)}) VALUES ({placeholders})"
        return sql
