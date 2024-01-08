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

    def __init__(self, upgrade_model: UpgradeModel, max_hp: int, power_usage: int, hp: Optional[int] = None, subscriptions: Optional[dict] = None) -> None:
        super().__init__(subscriptions=subscriptions)
        if max_hp < 1:
            max_hp = 1
        if hp is None:
            hp = max_hp
        if power_usage < 0:
            power_usage = 0

        self.upgrade_model = upgrade_model
        self.max_hp = max_hp
        self.hp = hp
        self.power_usage = power_usage

    def __setattr__(self, key, value) -> None:
        if key == "max_hp" and hasattr(self, "max_hp") and hasattr(self, "hp"):
            hp_increase = value - self.max_hp
            self.hp += hp_increase
        super().__setattr__(key, value)
    
    def to_dict(self) -> Response:
        data = {
            "max_hp": self.max_hp,
            "hp": self.hp,
            "power_usage": self.power_usage,
            "levels": self.upgrade_model.get_levels(),
            "model": self.upgrade_model.model_name
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
    
    def get_stats(self) -> Response:
        data = [
            ("health", f"{self.hp}/{self.max_hp}"),
            ("power_usage", str(self.power_usage))
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
            if not self.upgrade_model.has_upgrades(property=property):
                continue
            option = self.upgrade_model.get_upgrade_option(property=property)
            upgrade_options.append(option)
        return Response.create(upgrade_options, Response.TYPES.SYSTEM_UPGRADES)
    
    def upgrade_property(self, property: str) -> Response:
        if property not in self.upgrade_model.get_upgrades():
            raise RuntimeError(f"Tried to upgrade property {property} of system {self.NAME}, but the property is not upgradable")
        if not hasattr(self, property):
            raise RuntimeError(f"Tried to upgrade property {property} of system {self.NAME}, but the property does not exist in that ship system")
        if not self.upgrade_model.can_upgrade_property(property=property):
            raise RuntimeError(f"Tried to upgrade property {property} of system {self.NAME}, but the property is already at max level")
        
        current_level = self.upgrade_model.get_property_level(property=property)
        difference = self.upgrade_model.get_upgrade_difference(property=property, current_level=current_level)
        enhancements = self.upgrade_model.get_level_enhances(property=property, level=current_level+1)

        current_value = getattr(self, property)
        setattr(self, property, current_value + difference)

        for property_name, value in enhancements.items():
            if not hasattr(self, property_name):
                raise RuntimeError(f"Upgrade of property {property} in ship system {self.NAME} tried to also upgrade non-existent property {property_name}")
            property_value = getattr(self, property_name)
            setattr(self, property_name, property_value + value)

        cost = self.upgrade_model.get_level_cost(property=property, level=current_level+1)
        self.upgrade_model.upgrade_property(property=property)
        return Response.create(cost, Response.TYPES.UPGRADE_COST)
    
class SensorShipSystem(ShipSystem):
    REVEALED_DATA = []

    def __init__(self, upgrade_model: UpgradeModel, max_hp: int, power_usage: int, reveal_chance: Optional[int] = None, hp: Optional[int] = None) -> None:
        if reveal_chance is None:
            reveal_chance = 0
        self.reveal_chance = reveal_chance
        super().__init__(upgrade_model, max_hp, power_usage, hp)

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
        base_data = super().get_status().get_data()
        base_data.update({
            "success_rate": str(self.reveal_chance)+"%"
        })
        return Response.create(data=base_data)
    
    def get_stats(self) -> Response:
        base_data = super().get_stats().get_data()
        base_data.extend([
            ("success_rate", str(self.reveal_chance)+"%")   
        ])
        return Response.create(base_data)
    
    def get_revealed_data(self) -> Response:
        return Response.create(self.REVEALED_DATA)
    
    def to_dict(self) -> Response:
        base_dict: dict = super().to_dict().get_data()
        base_dict.update({
            "reveal_chance": self.reveal_chance
        })
        return Response.create(base_dict)