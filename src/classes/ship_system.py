from typing import Optional
from .event import Event
from .event_subscriber import BaseEventSubscriber
from .response import Response
from ..constants.custom_exceptions import EventTypeNotSubscribedError
from ..modules.validator import validate_int

class ShipSystem(BaseEventSubscriber):
    NAME = "default"

    def __init__(self, max_hp: int, hp: Optional[int] = None) -> None:
        super().__init__()
        if hp is None:
            hp = max_hp

        self.max_hp = max_hp
        self.hp = hp

    """
    Possible errors:
    - ValueError
    """
    @staticmethod
    def from_dict(system_name: str, data: dict) -> 'ShipSystem':
        return ShipSystemFactory.create(system_name=system_name, **data)
    
    def to_dict(self) -> dict:
        return {
            "max_hp": self.max_hp,
            "hp": self.hp
        }
    
    """
    Possible errors:
    - ValueError
    """
    def damage(self, amount: int) -> Response:
        validate_int(value=amount, value_name="amount", min_value=0)
        
        damage = amount
        initial_hp = self.hp

        self.hp -= amount
        if self.hp < 0:
            damage = initial_hp
            self.hp = 0

        return Response.create(f"{self.NAME.capitalize()} took {damage} damage.")
    
    # Whatever the ship system has to do every jump
    def work(self) -> Response:
        return Response.create()
    
    def get_name(self) -> str:
        return self.NAME
    
    def get_max_hp(self) -> int:
        return self.max_hp
    
    def get_hp(self) -> int:
        return self.hp

class HullSystem(ShipSystem):
    NAME = "hull"

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

    def charge(self, amount: int) -> Response:
        validate_int(value=amount, value_name="amount", min_value=0)
        
        charge = amount
        initial_capacity = self.capacity

        self.capacity += amount
        if self.capacity > self.max_capacity:
            charge = self.max_capacity - initial_capacity
            self.capacity = self.max_capacity
        
        return Response.create(f"Battery charged by {charge}")

    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            "max_capacity": self.max_capacity,
            "capacity": self.capacity
        })
        return base_dict
    
    def get_max_capacity(self) -> int:
        return self.max_capacity
    
    def get_capacity(self) -> int:
        return self.capacity

class SolarPanelSystem(ShipSystem):
    NAME = "solar panel"

    def __init__(self, max_hp: int, charge_capacity: int, hp: Optional[int] = None) -> None:
        self.charge_capacity = charge_capacity

        super().__init__(max_hp=max_hp, hp=hp)

    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            "charge_capacity": self.charge_capacity
        })
        return base_dict
    
    def work(self) -> Response:
        charge_event = Event(Event.TYPES.BATTERY_CHARGE, amount=self.charge_capacity)

        try:
            response = self.publish_event(event=charge_event)
        except EventTypeNotSubscribedError:
            return Response.create("Solar panel has no battery to charge.")
        
        return response
    
    def get_charge_capacity(self) -> int:
        return self.charge_capacity
    
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