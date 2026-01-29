import psycopg
from db.model_schema import ModelSchema
from db.types import RowData


def write_row(
    conn: psycopg.Connection,
    schema: ModelSchema,
    row: RowData,
) -> None:
    """
    Insert one logical row into a model-owned table.

    This function is generic: table-specific SQL is provided
    by the TableSchema.
    """
    table_schema = schema.get_table(row.table)

    if table_schema.is_static():
        raise ValueError(
            f"Attempted to write to static table '{row.table}'"
        )

    sql, params = table_schema.insert_statement(row.data)

    with conn.cursor() as cur:
        cur.execute(sql, params)

    conn.commit()
