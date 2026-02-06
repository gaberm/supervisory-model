from dataclasses import dataclass
from models.outputs.outputs_decorator import record


@record(
    table="charging_outputs",
    key=("vehicle_id",),
    indexed=("stop_time",),
)
@dataclass(frozen=True)
class VehicleSoc:
    vehicle_id: int
    soc: float
    stop_time: float


@dataclass(frozen=True)
class ChargingOutputs:
    vehicles_soc: tuple[VehicleSoc, ...]
