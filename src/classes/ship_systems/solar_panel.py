from typing import Optional

from src.classes.event import Event
from src.classes.response import Response
from src.classes.ship_system import ShipSystem
from src.constants.custom_exceptions import EventTypeNotSubscribedError

class SolarPanelSystem(ShipSystem):
    NAME = "solar panel"

    def __init__(self, max_hp: int, charge_capacity: int, hp: Optional[int] = None) -> None:
        self.charge_capacity = charge_capacity

        super().__init__(max_hp=max_hp, hp=hp)

    def to_dict(self) -> Response:
        base_dict: dict = super().to_dict().get_data()
        base_dict.update({
            "charge_capacity": self.charge_capacity
        })
        return Response.from_data(base_dict)
    
    def work(self) -> Response:
        charge_event = Event(Event.TYPES.BATTERY_CHARGE, amount=self.charge_capacity)

        try:
            response = self.publish_event(event=charge_event)
        except EventTypeNotSubscribedError:
            return Response.create("Solar panel has no battery to charge.", Response.TYPES.SHIP_STATUS_LOG)
        
        return response
    
    def get_charge_capacity(self) -> Response:
        return Response.from_data(self.charge_capacity)