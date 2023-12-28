import random
from typing import Optional
from .config import Config
from .event_subscriber import BaseEventSubscriber
from .response import Response
from ..modules.validator import validate_int

CONFIG = Config.get_instance()

class ShipSystem(BaseEventSubscriber):
    NAME = "default"

    def __init__(self, max_hp: int, hp: Optional[int] = None) -> None:
        super().__init__()
        if max_hp < 1:
            max_hp = 1
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

        return Response.create(f"{self.NAME.capitalize()} took {damage} damage.", Response.TYPES.SHIP_STATUS_LOG)
    
    def get_hp_percentage(self) -> Response:
        if self.max_hp == 0:
            percentage = 0
        else:
            percentage = round(self.hp/self.max_hp, CONFIG.DECIMAL_DIGITS)
        return Response.from_data(percentage)
    
    def get_current_status(self) -> Response:
        hp_percentage = self.get_hp_percentage().get_data()
        data = (self.NAME, hp_percentage)
        return Response.from_data(data=data)
    
    # Whatever the ship system has to do every jump
    def work(self) -> Response:
        return Response.create()
    
    def get_name(self) -> Response:
        return Response.from_data(self.NAME)
    
    def get_max_hp(self) -> Response:
        return Response.from_data(self.max_hp)
    
    def get_hp(self) -> Response:
        return Response.from_data(self.hp)
    
    def get_hp_ratio(self) -> Response:
        return Response.from_data(self.hp / self.max_hp)
    
class SensorShipSystem(ShipSystem):
    REVEALED_DATA = []

    def __init__(self, max_hp: int, reveal_chance: Optional[float] = None, hp: Optional[int] = None) -> None:
        if reveal_chance is None:
            reveal_chance = 0
        self.reveal_chance = reveal_chance
        super().__init__(max_hp, hp)

    def work(self) -> Response:
        hp_ratio = self.get_hp_ratio().get_data()
        data_revealed = random.random()
        data = []
        if data_revealed < self.reveal_chance * hp_ratio:
            data = self.REVEALED_DATA
        return Response.from_data(data, Response.TYPES.SCANNER_RESULT)
    
    def get_revealed_data(self) -> Response:
        return Response.from_data(self.REVEALED_DATA)
    
    def to_dict(self) -> Response:
        base_dict: dict = super().to_dict().get_data()
        base_dict.update({
            "reveal_chance": self.reveal_chance
        })
        return Response.from_data(base_dict)