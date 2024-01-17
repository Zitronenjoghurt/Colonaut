import math
from typing import Optional
from src.constants.config import Config
from src.events.event import Event
from src.events.response import Response
from src.planet_generation.unit_value import UnitValue
from src.space_ship.ship_system import ShipSystem
from src.space_ship.upgrade_model import UpgradeModel
from src.utils.maths import linear_interpolation
from src.utils.range import Range

CONFIG = Config.get_instance()

# Ranges for sustainable human survival without extensive equipment
HUMAN_TEMPERATURE_RANGE = Range(min=10, max=30)
HUMAN_GRAVITY_RANGE = Range(min=8.9, max=10.8)

# Score parameters
BASE_SCORE = 1000

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
            min_temperature: float,
            base_temperature: float,
            max_temperature: float,
            gravity_tolerance: int,
            min_gravity: float,
            base_gravity: float,
            max_gravity: float,
            hp: Optional[int] = None, 
            subscriptions: Optional[dict] = None
        ) -> None:
        subscriptions = {
            Event.TYPES.HABITATION_RETRIEVE_REPORT: self.get_report
        }
        super().__init__(upgrade_model, max_hp, power_usage, hp, subscriptions)
        self.temperature_tolerance = temperature_tolerance
        self.min_temperature = min_temperature
        self.base_temperature = base_temperature
        self.max_temperature = max_temperature

        self.gravity_tolerance = gravity_tolerance
        self.min_gravity = min_gravity
        self.base_gravity = base_gravity
        self.max_gravity = max_gravity
    
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
    
    def get_temperature_range(self) -> Range:
        return self.interpolate_tolerance(
            min=self.min_temperature,
            base=self.base_temperature,
            max=self.max_temperature,
            tolerance=self.temperature_tolerance
        )
    
    def get_gravity_range(self) -> Range:
        return self.interpolate_tolerance(
            min=self.min_gravity,
            base=self.base_gravity,
            max=self.max_gravity,
            tolerance=self.gravity_tolerance
        )
    
    @staticmethod
    def interpolate_tolerance(min: float, base: float, max: float, tolerance: int) -> Range:
        progress = tolerance/100
        min_tolerance = linear_interpolation(base, min, progress)
        max_tolerance = linear_interpolation(base, max, progress)
        tolerance_range = Range(min=min_tolerance, max=max_tolerance)
        return tolerance_range
    
    def get_report(self) -> Response:
        planet_report_event = Event(Event.TYPES.RETRIEVE_PLANET_REPORT)
        planet_report_response = self.publish_event(planet_report_event)
        planet_report = planet_report_response.get_data(Response.TYPES.PLANET_REPORT)

        report = {}

        temperature = planet_report.get("temperature", None)
        if isinstance(temperature, UnitValue):
            temperature = temperature.convert("°C")
            
            human_distance = HUMAN_TEMPERATURE_RANGE.get_relative_distance_to(value=temperature.get_value())
            human_score = self.calculate_score(human_distance)
            report["human_temperature_score"] = human_score
            report["human_temperature_percentage"] = human_score / BASE_SCORE * 100

            habitat_distance = self.get_temperature_range().get_relative_distance_to(value=temperature.get_value())
            habitat_score = self.calculate_score(habitat_distance)
            report["habitat_temperature_score"] = habitat_score
            report["habitat_temperature_percentage"] = habitat_score / BASE_SCORE * 100
        
        gravity = planet_report.get("gravity", None)
        if isinstance(gravity, UnitValue):
            gravity = gravity.convert("m/s^2")

            human_distance = HUMAN_GRAVITY_RANGE.get_relative_distance_to(value=gravity.get_value())
            human_score = self.calculate_score(human_distance)
            report["human_gravity_score"] = human_score
            report["human_gravity_percentage"] = human_score / BASE_SCORE * 100

            habitat_distance = self.get_gravity_range().get_relative_distance_to(value=gravity.get_value())
            habitat_score = self.calculate_score(habitat_distance)
            report["habitat_gravity_score"] = habitat_score
            report["habitat_gravity_percentage"] = habitat_score / BASE_SCORE * 100

        return Response.create(data=report, response_type=Response.TYPES.HABITATION_REPORT)
    
    @staticmethod
    def calculate_score(distance: float) -> float:
        score = BASE_SCORE - BASE_SCORE * math.log(distance*0.75 + 1)
        if score < 0:
            score = 0
        return score