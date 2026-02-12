from dataclasses import dataclass
from models.outputs.outputs_decorator import record


@record(
    table="charging_vehicles",
    key=("vehicle_id", "timestamp"),
    indexed=("timestamp",),
)
@dataclass(frozen=True)
class ChargingVehicle:
    vehicle_id: int
    soc: float
    timestamp: float


@record(
    table="charged_vehicles",
    key=("vehicle_id",),
    indexed=("ended_at",),
)
@dataclass(frozen=True)
class ChargedVehicle:
    vehicle_id: int
    soc: float
    ended_at: float


@dataclass(frozen=True)
class ChargingOutputs:
    charging_vehicles: tuple[ChargingVehicle, ...]
    charged_vehicles: tuple[ChargedVehicle, ...]
