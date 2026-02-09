from dataclasses import dataclass
from models.outputs.outputs_decorator import record


@record(
    table="charging",
    key=("vehicle_id",),
    indexed=("timestamp",),
)
@dataclass(frozen=True)
class ChargingState:
    vehicle_id: int
    soc: float
    timestamp: float


@record(
    table="charged",
    key=("vehicle_id",),
    indexed=("ended_at",),
)
@dataclass(frozen=True)
class ChargedState:
    vehicle_id: int
    soc: float
    ended_at: float


@dataclass(frozen=True)
class ChargingOutputs:
    charging: tuple[ChargingState, ...]
    charged: tuple[ChargedState, ...]
