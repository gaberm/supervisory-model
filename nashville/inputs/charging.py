from typing import TypedDict
from base.input.input import Input, Filter, Equal
from ..entities.vehicle import Vehicle


class VehicleSoc(TypedDict):
    veh_id: int
    soc: float


class ArrivedVehicles(Input):
    entity = Vehicle
    filters = [
        Filter(entity=Vehicle, field="status", cmp=Equal("arrived")),
    ]
    row = VehicleSoc


class DepartedVehicles(Input):
    entity = Vehicle
    filters = [
        Filter(entity=Vehicle, field="status", cmp=Equal("departed")),
    ]
    row = VehicleSoc
