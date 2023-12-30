from typing import Optional

from src.classes.display_text import DisplayText
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
        return Response.create(base_dict)
    
    def get_status(self) -> Response:
        hp_percentage = self.get_hp_percentage().get_data()
        data = {
            "health": hp_percentage,
            "Power": str(self.charge_capacity)
        }
        return Response.create(data=data)
    
    def work(self) -> Response:
        charge_event = Event(Event.TYPES.BATTERY_CHARGE, amount=self.charge_capacity)

        try:
            battery_message = self.publish_event(event=charge_event).get_data(Response.TYPES.SHIP_STATUS_LOG_ENTRY)
            message = DisplayText(f"[ENERGY] Solar panels collected {self.charge_capacity} energy units")
            if battery_message:
                message.add_text(battery_message.get_text())
            return Response.create(message, Response.TYPES.SHIP_STATUS_LOG_ENTRY)
        except EventTypeNotSubscribedError:
            message = DisplayText("[ENERGY] Solar panel has no battery to charge")
            return Response.create(message, Response.TYPES.SHIP_STATUS_LOG_ENTRY)
    
    def get_charge_capacity(self) -> Response:
        return Response.create(self.charge_capacity)