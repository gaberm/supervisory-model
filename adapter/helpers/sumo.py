import random
import pandas as pd


class EdgeToBuildingAssigner:
    def __init__(self, seed: int = 0):
        self.rng = random.Random(seed)

    def assign(self, edge_id: int) -> int:
        return self.rng.randint(1, 10000)  # Dummy building ID assignment


class TourIdLookup:
    def __init__(self):
        self.data = pd.read_csv("data/inputs/sumo/trips_person_6_7.csv")
        self.data = self.data[["id", "tour_id", "hhno", "pno", "dpurp"]]
        self.data.columns = [
            "vehicle_id",
            "tour_id",
            "household_no",
            "person_no",
            "departure_purpose",
        ]

    def get_tour_id(self, vehicle_id: int) -> int:
        row = self.data[self.data["vehicle_id"] == vehicle_id]
        if not row.empty:
            return int(row.iloc[0]["tour_id"])
        else:
            raise ValueError(f"Vehicle ID {vehicle_id} not found in trips data.")
