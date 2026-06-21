from base import Input, Fields
from nashville.outputs.charging import ChargingEvent


class VehicleSocInput(Input):
    from_ = ChargingEvent
    select = Fields("veh_id", "final_soc")
