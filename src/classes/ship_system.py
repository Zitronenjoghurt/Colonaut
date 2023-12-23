from typing import Callable, Optional
from .event_subscriber import BaseEventSubscriber
from .response import Response

class ShipSystem(BaseEventSubscriber):
    NAME = "default"

    def __init__(self, max_hitpoints: int, hitpoints: Optional[int] = None) -> None:
        if hitpoints is None:
            hitpoints = max_hitpoints

        self.max_hitpoints = max_hitpoints
        self.hitpoints = hitpoints

    """
    Possible errors:
    - ValueError
    """
    @staticmethod
    def from_dict(system_name: str, data: dict) -> 'ShipSystem':
        return ShipSystemFactory.create(system_name=system_name, **data)
    
    def to_dict(self) -> dict:
        return {
            "max_hitpoints": self.max_hitpoints,
            "hitpoints": self.hitpoints
        }
    
    """
    Possible errors:
    - ValueError
    """
    def damage(self, amount: int) -> Response:
        if not isinstance(amount, int):
            raise ValueError("Amount must be of type int.")
        if amount < 0:
            raise ValueError("Amount must be greater or equal 0.")
        self.hitpoints -= amount

        if self.hitpoints < 0:
            self.hitpoints = 0

        return Response.create()
    
    def get_name(self) -> str:
        return self.NAME
    
    def get_max_hitpoints(self) -> int:
        return self.max_hitpoints
    
    def get_hitpoints(self) -> int:
        return self.hitpoints

class HullSystem(ShipSystem):
    NAME = "hull"

class BatterySystem(ShipSystem):
    NAME = "battery"

    def __init__(self, max_hitpoints: int, max_capacity: int, hitpoints: Optional[int] = None, capacity: Optional[int] = None) -> None:
        if capacity is None:
            capacity = max_capacity

        self.max_capacity = max_capacity
        self.capacity = capacity

        super().__init__(max_hitpoints=max_hitpoints, hitpoints=hitpoints)

    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            "max_capacity": self.max_capacity,
            "capacity": self.capacity
        })
        return base_dict

class SolarPanelSystem(ShipSystem):
    NAME = "solar panel"

    def __init__(self, max_hitpoints: int, charge_capacity: int) -> None:
        self.charge_capacity = charge_capacity

        super().__init__(max_hitpoints=max_hitpoints)

    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            "charge_capacity": self.charge_capacity
        })
        return base_dict
    
class ShipSystemFactory():
    REGISTRY = {
        "hull": HullSystem,
        "battery": BatterySystem,
        "solar panel": SolarPanelSystem
    }

    """
    Possible errors:
    - ValueError
    """
    @staticmethod
    def create(system_name: str, **kwargs) -> 'ShipSystem':
        system_name = system_name.lower()
        system_class = ShipSystemFactory.REGISTRY.get(system_name, None)

        if system_class is None:
            raise ValueError(f"Ship system {system_name} not found.")
        try:
            return system_class(**kwargs)
        except TypeError as e:
            raise ValueError(f"An error occured while creating system {system_name}: {e}")