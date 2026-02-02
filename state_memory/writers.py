import psycopg
from traitlets import Any
from schemas.db.model_schema import ModelSchema


def create_tables(
    conn: psycopg.Connection,
    schema: ModelSchema,
) -> None:
    with conn.cursor() as cur:
        for table in schema.tables().values():
            cur.execute(table.create_sql())
    conn.commit()


def write_row(
    conn: psycopg.Connection,
    schema: ModelSchema,
    row: tuple[Any],
) -> None:
    table_schema = schema.get_table(row.table)
    sql = table_schema.insert_sql()
    with conn.cursor() as cur:
        cur.execute(sql, row.data)
    conn.commit()
