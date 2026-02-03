from dataclasses import dataclass
from models.outputs.decorator import record


@record(
    table="charging_outputs",
    key=("time_index",),
    indexed=("vehicle_id",),
)
@dataclass(frozen=True)
class VehicleSoc:
    vehicle_id: int
    soc: float


@dataclass(frozen=True)
class ChargingOutputs:
    vehicles_soc: tuple[VehicleSoc, ...]
