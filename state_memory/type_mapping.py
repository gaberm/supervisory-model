from datetime import datetime

PYTHON_TO_SQL = {
    int: "INTEGER",
    float: "DOUBLE PRECISION",
    str: "TEXT",
    bool: "BOOLEAN",
    datetime: "TIMESTAMP",
}


def sql_type(py_type):
    try:
        return PYTHON_TO_SQL[py_type]
    except KeyError:
        raise TypeError(f"Unsupported field type: {py_type}")
