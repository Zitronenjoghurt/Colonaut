from typing import Optional
from .event_subscriber import BaseEventSubscriber
from .response import Response

from ..modules.validator import validate_int

class ShipSystem(BaseEventSubscriber):
    NAME = "default"

    def __init__(self, max_hp: int, hp: Optional[int] = None) -> None:
        super().__init__()
        if hp is None:
            hp = max_hp

        self.max_hp = max_hp
        self.hp = hp
    
    def to_dict(self) -> Response:
        data = {
            "max_hp": self.max_hp,
            "hp": self.hp
        }
        return Response.from_data(data)
    
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
    
    def get_name(self) -> Response:
        return Response.from_data(self.NAME)
    
    def get_max_hp(self) -> Response:
        return Response.from_data(self.max_hp)
    
    def get_hp(self) -> Response:
        return Response.from_data(self.hp)