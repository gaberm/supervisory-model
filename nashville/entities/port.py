from dataclasses import dataclass
from typing import Optional
from base.entity.entity import Entity


@dataclass
class Port(Entity):
    table_name = "ports"
    primary_key = ("port_id", "station_id")
    indexed = ("h3", "status", "time")

    port_id: str
    station_id: str
    power_usage: float
    status: str
    time: float
    h3: Optional[str] = None
