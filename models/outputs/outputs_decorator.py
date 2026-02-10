from typing import Tuple


def record(
    *,
    table: str,
    key: Tuple[str, ...],
    indexed: Tuple[str, ...] = (),
):
    """
    ...

    Parameters:
      table   – database table name
      key     – primary key fields
      indexed – fields to index
    """

    def decorator(cls):
        # --- Attach metadata only ---
        cls.__record__ = {
            "table": table,
            "key": key,
            "indexed": indexed,
        }
        return cls

    return decorator
