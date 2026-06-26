from dataclasses import dataclass
from base import Record
from base.output.timestamp import Timestamp

RUN_ID = "run_test"


@dataclass(kw_only=True)
class Vehicle(Record, Timestamp):
    table_name = "vehicle"
    primary_key = ("veh_id",)
    veh_id: str
    soc: float


@dataclass(kw_only=True)
class Battery(Record):
    table_name = "battery"
    primary_key = ("veh_id",)
    veh_id: str
    capacity: float
