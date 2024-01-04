from typing import Optional

from src.ui.display_text import DisplayText
from src.events.event import Event
from src.events.response import Response
from src.space_ship.ship_system import ShipSystem
from src.utils.validator import validate_int

class BatterySystem(ShipSystem):
    NAME = "battery"

    def __init__(self, max_hp: int, max_capacity: int, hp: Optional[int] = None, capacity: Optional[int] = None) -> None:
        subscriptions = {
            Event.TYPES.BATTERY_CHARGE: self.charge
        }
        if capacity is None:
            capacity = max_capacity

        self.max_capacity = max_capacity
        self.capacity = capacity

        super().__init__(max_hp=max_hp, hp=hp, subscriptions=subscriptions)

    """
    Possible errors:
    - ValueError
    """
    def charge(self, amount: int) -> Response:
        validate_int(value=amount, value_name="amount", min_value=0)
        
        charge = amount
        initial_capacity = self.capacity

        self.capacity += amount
        if self.capacity > self.max_capacity:
            charge = self.max_capacity - initial_capacity
            self.capacity = self.max_capacity

        message = f"Battery charged by {charge}"
        if charge == 0:
            message = "Battery fully charged"
        message = DisplayText(message, character="energy")
        
        return Response.create(message, Response.TYPES.SHIP_STATUS_LOG_ENTRY)

    def to_dict(self) -> Response:
        base_dict: dict = super().to_dict().get_data()
        base_dict.update({
            "max_capacity": self.max_capacity,
            "capacity": self.capacity
        })
        return Response.create(base_dict)
    
    def get_status(self) -> Response:
        hp_percentage = self.get_hp_percentage().get_data()
        data = {
            "health": hp_percentage,
            "Capacity": f"{self.capacity}/{self.max_capacity}"
        }
        return Response.create(data=data)
    
    def get_max_capacity(self) -> Response:
        return Response.create(self.max_capacity)
    
    def get_capacity(self) -> Response:
        return Response.create(self.capacity)