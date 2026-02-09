from dataclasses import dataclass


@dataclass(frozen=True)
class TimeRange:
    start_time: float
    end_time: float
