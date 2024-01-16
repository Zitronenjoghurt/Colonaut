from typing import Optional

from src.constants.custom_exceptions import EventTypeNotSubscribedError
from src.constants.locale_translator import LocaleTranslator
from src.events.event import Event
from src.events.response import Response
from src.space_ship.ship_system import ShipSystem
from src.space_ship.upgrade_model import UpgradeModel
from src.ui.display_text import DisplayText
from src.utils.validator import validate_int

LT = LocaleTranslator.get_instance()

class BatterySystem(ShipSystem):
    NAME = "battery"
    DASHBOARD_ORDER_PRIORITY = 90
    WORK_ORDER_PRIORITY = -100

    def __init__(self, upgrade_model: UpgradeModel, max_hp: int, max_capacity: int, power_usage: int = 0, hp: Optional[int] = None, capacity: Optional[int] = None) -> None:
        subscriptions = {
            Event.TYPES.BATTERY_CHARGE: self.charge,
            Event.TYPES.BATTERY_DRAW_ENERGY: self.draw_energy,
            Event.TYPES.BATTERY_RETRIEVE_DRAWN_ENERGY_LOG: self.retrieve_drawn_energy_log
        }
        if capacity is None:
            capacity = max_capacity

        self.max_capacity = max_capacity
        self.capacity = capacity
        self.drawn_energy = 0

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

        message = LT.get(LT.KEYS.BATTERY_CHARGED_BY, charge=charge)
        if charge == 0:
            message = LT.get(LT.KEYS.BATTERY_FULLY_CHARGED)
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
    
    def draw_energy(self, amount: int, system_name: str) -> Response:
        if amount > self.capacity:
            game_over = Event(Event.TYPES.GAME_OVER_NO_ENERGY, system_name=system_name)
            self.publish_event(game_over)
            return Response.create()
        self.capacity -= amount
        self.drawn_energy += amount
        return Response.create()
    
    def retrieve_drawn_energy_log(self) -> Response:
        charge_capacity_event = Event(Event.TYPES.SOLAR_PANEL_RETRIEVE_CHARGE_CAPACITY)
        try:
            response = self.publish_event(charge_capacity_event)
            charge_capacity = response.get_data()
        except EventTypeNotSubscribedError:
            charge_capacity = None

        messages = [DisplayText(LT.get(LT.KEYS.BATTERY_DISTRIBUTED_ENERGY, drawn_energy=self.drawn_energy), character="energy")]
        if isinstance(charge_capacity, int) and charge_capacity < self.drawn_energy:
            messages.append(DisplayText(LT.get(LT.KEYS.BATTERY_WARNING_NET_NEGATIVE_ENERGY), character="energy", tag="warning"))
        
        self.drawn_energy = 0
        return Response.create(messages, Response.TYPES.BATTERY_DRAWN_ENERGY_LOG)