import random
from typing import Any, Optional
from src.constants.config import Config
from src.constants.locale_translator import LocaleTranslator
from src.ui.display_text import DisplayText
from src.events.event_subscriber import BaseEventSubscriber
from src.events.response import Response
from src.space_ship.upgrade_model import UpgradeModel
from src.utils.validator import validate_int

CONFIG = Config.get_instance()
LT = LocaleTranslator.get_instance()

class ShipSystem(BaseEventSubscriber):
    NAME = "default"

    def __init__(self, upgrade_model: UpgradeModel, max_hp: int, hp: Optional[int] = None, subscriptions: Optional[dict] = None) -> None:
        super().__init__(subscriptions=subscriptions)
        if max_hp < 1:
            max_hp = 1
        if hp is None:
            hp = max_hp
        
        self.upgrade_model = upgrade_model
        self.max_hp = max_hp
        self.hp = hp

    def __setattr__(self, key, value) -> None:
        if key == "max_hp" and hasattr(self, "max_hp") and hasattr(self, "hp"):
            hp_increase = value - self.max_hp
            self.hp += hp_increase
        super().__setattr__(key, value)
    
    def to_dict(self) -> Response:
        data = {
            "max_hp": self.max_hp,
            "hp": self.hp
        }
        self.upgraded_properties_to_dict(data)
        return Response.create(data)
    
    def get_property_value(self, property: str) -> Any:
        if hasattr(self, property) and not callable(getattr(self, property)) and not property.startswith('__'):
            return getattr(self, property)
        else:
            raise ValueError(f"Ship system {self.NAME} has no property {property}")
    
    def upgraded_properties_to_dict(self, data: dict) -> None:
        for property in data:
            if property in self.upgrade_model.get_upgrades():
                value = data[property]
                if not isinstance(value, int):
                    continue
                level = self.upgrade_model.get_value_level(property=property, value=value)
                data[property] = str(level)
    
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
    
    def get_stats(self) -> Response:
        data = [
            ("Health", f"{self.hp}/{self.max_hp}")
        ]
        return Response.create(data=data)
    
    # Whatever the ship system has to do every jump
    def work(self) -> Response:
        return Response.create()
    
    def get_name(self) -> Response:
        return Response.create(self.NAME)
    
    def get_description(self) -> Response:
        return Response.create(LT.get(self.NAME+"_description"))
    
    def get_max_hp(self) -> Response:
        return Response.create(self.max_hp)
    
    def get_hp(self) -> Response:
        return Response.create(self.hp)
    
    def get_hp_ratio(self) -> Response:
        return Response.create(self.hp / self.max_hp)
    
    def get_system_window_data(self) -> Response:
        stats = self.get_stats().get_data()
        data = {
            'description': self.get_description().get_data(),
            'stats': stats
        }
        return Response.create(data, Response.TYPES.SYSTEM_WINDOW_DATA)
    
    def get_upgrades(self) -> Response:
        upgrade_options = []
        for property in self.upgrade_model.get_upgrades():
            option = self.upgrade_model.get_upgrade_option(property=property, value=self.get_property_value(property=property))
            upgrade_options.append(option)
        return Response.create(upgrade_options, Response.TYPES.SYSTEM_UPGRADES)
    
    def upgrade_property(self, property: str) -> Response:
        if property not in self.upgrade_model.get_upgrades():
            raise RuntimeError(f"Tried to upgrade property {property} of system {self.NAME}, but the property is not upgradable.")
        current_level = self.upgrade_model.get_value_level(property=property, value=self.get_property_value(property=property))
        new_value = self.upgrade_model.get_level_value(property=property, level=current_level+1)
        cost = self.upgrade_model.get_level_cost(property=property, level=current_level+1)
        setattr(self, property, new_value)
        return Response.create(cost, Response.TYPES.UPGRADE_COST)
    
class SensorShipSystem(ShipSystem):
    REVEALED_DATA = []

    def __init__(self, upgrade_model: UpgradeModel, max_hp: int, reveal_chance: Optional[int] = None, hp: Optional[int] = None) -> None:
        if reveal_chance is None:
            reveal_chance = 0
        self.reveal_chance = reveal_chance
        super().__init__(upgrade_model, max_hp, hp)

    def work(self) -> Response:
        hp_ratio = self.get_hp_ratio().get_data()
        data_revealed = random.random()
        data = []

        messages = [DisplayText(f"{self.NAME.capitalize()}: ", character= "sensor", line_delay=300, newline=False)]
        if data_revealed < (self.reveal_chance/100) * hp_ratio:
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
            "Success rate": str(self.reveal_chance)+"%"
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