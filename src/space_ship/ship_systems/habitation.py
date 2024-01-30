import math
from typing import Optional
from src.constants.config import Config
from src.events.event import Event
from src.events.response import Response
from src.planet_generation.atmosphere import Atmosphere
from src.planet_generation.unit_value import UnitValue
from src.space_ship.ship_system import ShipSystem
from src.space_ship.upgrade_model import UpgradeModel
from src.utils.maths import clam, linear_interpolation
from src.utils.range import Range

CONFIG = Config.get_instance()

HABITABILITY_CONFIG = {
    "temperature": {
        # Ranges for sustainable human survival without extensive equipment
        "min_human_range": 10,
        "max_human_range": 30,
        # If youre that far away from the sustainable parameters, youll have a score of exact 0
        "score_max_distance": 20,
        # If youre that far away from the sustainable parameters, youll have a percentage of 0%
        "percentage_max_distance": 40
    },
    "gravity": {
        "min_human_range": 8.9,
        "max_human_range": 10.8,
        "score_max_distance": 1.5,
        "percentage_max_distance": 2
    }
}

HUMAN_TEMPERATURE_RANGE = Range(
    min=HABITABILITY_CONFIG["temperature"]["min_human_range"], 
    max=HABITABILITY_CONFIG["temperature"]["max_human_range"]
)
HUMAN_GRAVITY_RANGE = Range(
    min=HABITABILITY_CONFIG["gravity"]["min_human_range"], 
    max=HABITABILITY_CONFIG["gravity"]["max_human_range"]
)

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
            
            human_distance = HUMAN_TEMPERATURE_RANGE.get_distance_to(value=temperature.get_value())
            human_score, human_percentage = self.calculate_score_percentage(human_distance, "temperature")
            report["human_temperature_score"] = human_score
            report["human_temperature_percentage"] = human_percentage

            habitat_distance = self.get_temperature_range().get_distance_to(value=temperature.get_value())
            habitat_score, habitat_percentage = self.calculate_score_percentage(habitat_distance, "temperature")
            report["habitat_temperature_score"] = habitat_score
            report["habitat_temperature_percentage"] = habitat_percentage
        
        gravity = planet_report.get("gravity", None)
        if isinstance(gravity, UnitValue):
            gravity = gravity.convert("m/s^2")

            human_distance = HUMAN_GRAVITY_RANGE.get_relative_distance_to(value=gravity.get_value())
            human_score, human_percentage = self.calculate_score_percentage(human_distance, "gravity")
            report["human_gravity_score"] = human_score
            report["human_gravity_percentage"] = human_percentage

            habitat_distance = self.get_gravity_range().get_relative_distance_to(value=gravity.get_value())
            habitat_score, habitat_percentage = self.calculate_score_percentage(habitat_distance, "gravity")
            report["habitat_gravity_score"] = habitat_score
            report["habitat_gravity_percentage"] = habitat_percentage

        atmosphere = planet_report.get("atmosphere", None)
        if isinstance(atmosphere, Atmosphere) and isinstance(temperature, UnitValue):
            human_score, _ = atmosphere.get_breathability(temperature=temperature)

            report["human_breathability_percentage"] = human_score

            habitat_score = 0 if atmosphere.is_radioactive() else 100
            report["habitat_breathability_percentage"] = habitat_score

        return Response.create(data=report, response_type=Response.TYPES.HABITATION_REPORT)
    
    @staticmethod
    def calculate_score_percentage(distance: float, property: str) -> tuple[float, float]:
        try:
            score_max_distance = HABITABILITY_CONFIG[property]["score_max_distance"]
            percentage_max_distance = HABITABILITY_CONFIG[property]["percentage_max_distance"]
        except Exception as e:
            raise RuntimeError(f"An error occured while retrieving the habitability configuration for property '{property}': {e}")
        
        score = (score_max_distance - distance)/score_max_distance * BASE_SCORE
        percentage = (percentage_max_distance - distance)/percentage_max_distance * 100

        score = clam(score, 0, BASE_SCORE)
        percentage = clam(percentage, 0, 100)

        return score, percentage