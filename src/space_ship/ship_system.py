import random
from typing import Optional
from src.constants.config import Config
from src.ui.display_text import DisplayText
from src.events.event_subscriber import BaseEventSubscriber
from src.events.response import Response
from src.modules.validator import validate_int

CONFIG = Config.get_instance()

class ShipSystem(BaseEventSubscriber):
    NAME = "default"

    def __init__(self, max_hp: int, hp: Optional[int] = None, subscriptions: Optional[dict] = None) -> None:
        super().__init__(subscriptions=subscriptions)
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
        return Response.create(data)
    
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

        return Response.create([f"{self.NAME.capitalize()} took {damage} damage."], Response.TYPES.SHIP_STATUS_LOG_ENTRY)
    
    def get_hp_percentage(self) -> Response:
        if self.max_hp == 0:
            percentage = 0
        else:
            percentage = round(self.hp/self.max_hp, CONFIG.DECIMAL_DIGITS)
        return Response.create(percentage)
    
    def get_status(self) -> Response:
        hp_percentage = self.get_hp_percentage().get_data()
        data = {
            "health": hp_percentage
        }
        return Response.create(data=data)
    
    # Whatever the ship system has to do every jump
    def work(self) -> Response:
        return Response.create()
    
    def get_name(self) -> Response:
        return Response.create(self.NAME)
    
    def get_max_hp(self) -> Response:
        return Response.create(self.max_hp)
    
    def get_hp(self) -> Response:
        return Response.create(self.hp)
    
    def get_hp_ratio(self) -> Response:
        return Response.create(self.hp / self.max_hp)
    
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

        messages = [DisplayText(f"{self.NAME.capitalize()}: ", character= "sensor", line_delay=300, newline=False)]
        if data_revealed < self.reveal_chance * hp_ratio:
            data = self.REVEALED_DATA
            messages.append(DisplayText("SUCCESS", tag="success", line_symbol=False))
        else:
            messages.append(DisplayText("FAILURE", tag="failure", line_symbol=False))

        response = Response.create(data, Response.TYPES.SCANNER_RESULT)
        response.add_data(messages, Response.TYPES.SHIP_STATUS_LOG_ENTRY)
        return response
    
    def get_status(self) -> Response:
        hp_percentage = self.get_hp_percentage().get_data()
        data = {
            "health": hp_percentage,
            "Success rate": str(self.reveal_chance*100)+"%"
        }
        return Response.create(data=data)
    
    def get_revealed_data(self) -> Response:
        return Response.create(self.REVEALED_DATA)
    
    def to_dict(self) -> Response:
        base_dict: dict = super().to_dict().get_data()
        base_dict.update({
            "reveal_chance": self.reveal_chance
        })
        return Response.create(base_dict)