from traitlets import Any
from adapters import ModelAdapter
import traci
import re
from adapters.helpers.sumo import EdgeToBuildingAssigner, TourIdLookup
from ..schemas.adapters.sumo import SumoOutputs


class SumoAdapter(ModelAdapter):
    def __init__(
        self,
        name: str,
        timestep_length: int,
        sumo_config: str,
        building_assigner: EdgeToBuildingAssigner,
        tour_lookup: TourIdLookup,
    ):
        super().__init__(name, timestep_length)
        self.sumo_config = sumo_config
        self.building_assigner = building_assigner
        self.tour_lookup = tour_lookup

        self._traci = None
        self._last_pos = {}
        self._prev_vehicles = set()
        self._current_time = 0.0

    def current_time(self) -> float:
        return self._current_time

    def initialize(self):
        traci.start(["sumo", "-c", self.sumo_config])
        self._traci = traci
        self.timestep_length = traci.simulation.getDeltaT()

    def read_outputs(self) -> SumoOutputs:
        current_vehicles = set(traci.vehicle.getIDList())
        for vehicle_id in current_vehicles:
            try:
                id = int(re.sub(r"^(person_|truck_)", "", vehicle_id))
                road_id = traci.vehicle.getSubscriptionResults(vehicle_id)[
                    traci.constants.VAR_ROAD_ID
                ]
                self._last_pos[id] = road_id
            except traci.exceptions.TraCIException:
                pass
        spawned_vehicles = list(current_vehicles - self._prev_vehicles)
        self._prev_vehicles = current_vehicles

        arrival_buildings = {}
        for vehicle_id in traci.simulation.getArrivedIDList():
            vehicle_id = int(re.sub(r"^(person_|truck_)", "", vehicle_id))
            arrival_edge = self._last_pos.get(vehicle_id, None)
            arrival_buildings[vehicle_id] = self.building_assigner.assign(arrival_edge)

        return SumoOutputs(
            spawned_vehicles=spawned_vehicles, arrival_buildings=arrival_buildings
        )

    def advance(self, dt: float):
        if dt % self.timestep_length != 0:
            raise ValueError(
                f"SUMO adapter cannot advance by dt={dt}. It must be a multiple of the timestep length {self.timestep_length}."
            )

        steps = int(dt / self.timestep_length)
        for _ in range(steps):
            self._traci.simulationStep()
            self._current_time += self.timestep_length
