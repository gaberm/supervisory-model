from dataclasses import dataclass
from typing import ClassVar


@dataclass(kw_only=True)
class Timestamp:
    time: float | int
    time_field: ClassVar[str] = "time"

    def __post_init__(self):
        if not isinstance(self.time, (float, int)):
            raise TypeError(
                f"{type(self).__name__}.{self.time_field} must be a float or int"
            )
        if self.time < 0:
            raise ValueError(
                f"{type(self).__name__}.{self.time_field} must be non-negative"
            )

    def __init_subclass__(cls):
        all_annotations = {
            name
            for parent in cls.__mro__
            for name in getattr(parent, "__annotations__", {})
        }
        if cls.time_field not in all_annotations:
            raise TypeError(f"time_field must be a field in {cls.__name__}")
