from typing import Optional

from src.ui.display_text import DisplayText
from src.events.event import Event
from src.events.response import Response
from src.space_ship.ship_system import ShipSystem
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
        base_data = super().get_status().get_data()
        base_data.update({
            "Power": str(self.charge_capacity)
        })
        return Response.create(base_data)
    
    def get_stats(self) -> Response:
        base_data = super().get_stats().get_data()
        base_data.extend([
            ("Charge Capacity", str(self.charge_capacity))
        ])
        return Response.create(base_data)
    
    def work(self) -> Response:
        charge_event = Event(Event.TYPES.BATTERY_CHARGE, amount=self.charge_capacity)

        try:
            battery_message = self.publish_event(event=charge_event).get_data(Response.TYPES.SHIP_STATUS_LOG_ENTRY)
            messages = [DisplayText(f"Solar panels collected {self.charge_capacity} energy units", character="energy")]
            if battery_message:
                messages.append(battery_message)
            return Response.create(messages, Response.TYPES.SHIP_STATUS_LOG_ENTRY)
        except EventTypeNotSubscribedError:
            message = DisplayText("Solar panel has no battery to charge", character="energy")
            return Response.create(message, Response.TYPES.SHIP_STATUS_LOG_ENTRY)
    
    def get_charge_capacity(self) -> Response:
        return Response.create(self.charge_capacity)