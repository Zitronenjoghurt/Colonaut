from typing import Optional
from src.constants.config import Config
from src.events.event import Event
from src.events.response import Response
from src.space_ship.ship_system import ShipSystem
from src.space_ship.upgrade_model import UpgradeModel

CONFIG = Config.get_instance()

class HabitationSystem(ShipSystem):
    NAME = "habitation"
    DASHBOARD_ORDER_PRIORITY = 70
    WORK_ORDER_PRIORITY = -70

    def __init__(
            self, 
            upgrade_model: UpgradeModel, 
            max_hp: int, 
            power_usage: int, 
            temperature_tolerance: int, 
            gravity_tolerance: int, 
            hp: Optional[int] = None, 
            subscriptions: Optional[dict] = None
        ) -> None:
        super().__init__(upgrade_model, max_hp, power_usage, hp, subscriptions)
        self.temperature_tolerance = temperature_tolerance
        self.gravity_tolerance = gravity_tolerance

    def work(self) -> Response:
        planet_data_event = Event(Event.TYPES.RETRIEVE_PLANET_DATA, do_gibber=False)
        planet_data_response = self.publish_event(planet_data_event)
        planet_data = planet_data_response.get_data(Response.TYPES.PLANET_DATA)
        return Response.create()
    
    def to_dict(self) -> Response:
        base_dict: dict = super().to_dict().get_data()
        base_dict.update({
            "temperature_tolerance": self.temperature_tolerance,
            "gravity_tolerance": self.gravity_tolerance
        })
        return Response.create(base_dict)

    def get_status(self) -> Response:
        base_data = super().get_status().get_data()
        avg_tolerance = round((self.temperature_tolerance + self.gravity_tolerance)/2, CONFIG.DECIMAL_DIGITS)
        base_data.update({
            "average_tolerance": str(avg_tolerance)+"%"
        })
        return Response.create(base_data)
    
    def get_stats(self) -> Response:
        base_data = super().get_stats().get_data()
        base_data.extend([
            ("temperature_tolerance", str(self.temperature_tolerance)+"%"),
            ("gravity_tolerance", str(self.gravity_tolerance)+"%")
        ])
        return Response.create(base_data)