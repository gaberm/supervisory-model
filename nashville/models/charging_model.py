from typing import Dict


class ChargingModel:
    def __init__(self, charging_rate: float):
        self.charging_rate = charging_rate
        self.vehicles: Dict[int, float] = {}

    def add_vehicle(self, vehicle_id: int, initial_soc: float):
        self.vehicles[vehicle_id] = initial_soc

    def remove_vehicle(self, vehicle_id: int):
        if vehicle_id in self.vehicles:
            del self.vehicles[vehicle_id]

    def charge(self):
        # Simple charging logic: increase SOC by charging_rate
        for vehicle_id in self.vehicles:
            self.vehicles[vehicle_id] = min(
                100.0, self.vehicles[vehicle_id] + self.charging_rate
            )

    def get_soc(self, vehicle_id: int) -> float:
        return self.vehicles.get(vehicle_id, 0.0)

    def get_all_soc(self) -> dict[int, float]:
        return self.vehicles
