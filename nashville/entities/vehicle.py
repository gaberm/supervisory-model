from dataclasses import dataclass
from typing import Optional
from base.entity.entity import Entity


@dataclass
class Vehicle(Entity):
    table_name = "vehicles"
    primary_key = ("veh_id",)
    indexed = ("h3", "state", "time")

    veh_id: int
    soc: float | None
    state: str
    time: float
    lon: float
    lat: float
    h3: Optional[str] = None
