from __future__ import annotations
from abc import abstractmethod
from dataclasses import dataclass
from enum import StrEnum
from typing import ClassVar, Optional
from records.validation import validate_shape


class ShapeType(StrEnum):
    POINT = "point"
    POLYGON = "polygon"
    LINESTRING = "linestring"
    GLOBAL = "global"


@dataclass(frozen=True, kw_only=True)
class BaseRecord:
    table_name: ClassVar[str]
    primary_key: ClassVar[tuple[str, ...]]
    indexed: ClassVar[tuple[str, ...]] = ()
    domain: ClassVar[Optional[str]] = None
    diagnostic: ClassVar[bool] = False

    global_time: float
    shape_type: ShapeType
    shape_coord: list[tuple[float, float]]
    height: Optional[float] = None
    cell_ids: Optional[list[str]] = None

    def __post_init__(self):
        validate_shape(self.shape_coord, self.shape_type)

    @classmethod
    @abstractmethod
    def from_dict(cls, d: dict) -> BaseRecord: ...
