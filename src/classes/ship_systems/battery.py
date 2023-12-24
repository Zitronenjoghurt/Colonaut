from typing import Optional

from src.classes.event import Event
from src.classes.response import Response
from src.classes.ship_system import ShipSystem
from src.modules.validator import validate_int

class BatterySystem(ShipSystem):
    NAME = "battery"

    def __init__(self, max_hp: int, max_capacity: int, hp: Optional[int] = None, capacity: Optional[int] = None) -> None:
        self.SUBSCRIPTIONS = {
            Event.TYPES.BATTERY_CHARGE: self.charge
        }
        if capacity is None:
            capacity = max_capacity

        self.max_capacity = max_capacity
        self.capacity = capacity

        super().__init__(max_hp=max_hp, hp=hp)

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
        
        return Response.from_message(f"Battery charged by {charge}")

    def to_dict(self) -> Response:
        base_dict: dict = super().to_dict().get_data()
        base_dict.update({
            "max_capacity": self.max_capacity,
            "capacity": self.capacity
        })
        return Response.from_data(base_dict)
    
    def get_max_capacity(self) -> Response:
        return Response.from_data(self.max_capacity)
    
    def get_capacity(self) -> Response:
        return Response.from_data(self.capacity)