from typing import TypedDict
from base.input.input import Input, Filter, Equal
from nashville.entities.port import Port


class VehicleSoc(TypedDict):
    veh_id: int
    soc: float


class VehicleSocInput(Input):
    entity = Port
    filters = [
        Filter(entity=Port, field="status", cmp=Equal("arrived")),
    ]
    row = VehicleSoc
