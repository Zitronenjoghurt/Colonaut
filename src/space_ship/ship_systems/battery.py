from typing import Optional

from src.ui.display_text import DisplayText
from src.events.event import Event
from src.events.response import Response
from src.space_ship.ship_system import ShipSystem
from src.space_ship.upgrade_model import UpgradeModel
from src.utils.validator import validate_int

class BatterySystem(ShipSystem):
    NAME = "battery"

    def __init__(self, upgrade_model: UpgradeModel, max_hp: int, max_capacity: int, power_usage: int = 0, hp: Optional[int] = None, capacity: Optional[int] = None) -> None:
        subscriptions = {
            Event.TYPES.BATTERY_CHARGE: self.charge
        }
        if capacity is None:
            capacity = max_capacity

        self.max_capacity = max_capacity
        self.capacity = capacity

        super().__init__(upgrade_model=upgrade_model, max_hp=max_hp, power_usage=power_usage, hp=hp, subscriptions=subscriptions)

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
        base_data = super().get_status().get_data()
        base_data.update({
            "capacity": f"{self.capacity}/{self.max_capacity}"
        })
        return Response.create(base_data)
    
    def get_stats(self) -> Response:
        base_data = super().get_stats().get_data()
        base_data.extend([
            ("capacity", f"{self.capacity}/{self.max_capacity}")   
        ])
        return Response.create(base_data)
    
    def get_max_capacity(self) -> Response:
        return Response.create(self.max_capacity)
    
    def get_capacity(self) -> Response:
        return Response.create(self.capacity)