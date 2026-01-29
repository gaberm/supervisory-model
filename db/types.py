from dataclasses import dataclass
from typing import Mapping, Any


@dataclass(frozen=True)
class RowData:
    """
    Logical representation of one row to be inserted into a table.
    """
    table: str
    data: Mapping[str, Any]