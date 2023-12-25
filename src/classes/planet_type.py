import os
import random
from typing import Optional
from .config import Config
from .unit_value import UnitValue
from ..modules.utilities import file_to_dict

CONFIG = Config.get_instance()
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

class PlanetType():
    def __init__(self, 
                 min_temperature: UnitValue, 
                 max_temperature: UnitValue, 
                 min_radius: UnitValue, 
                 max_radius: UnitValue, 
                 min_density: UnitValue, 
                 max_density: UnitValue,
                 min_rot_period: UnitValue,
                 max_rot_period: UnitValue,
                 min_orb_period: UnitValue,
                 max_orb_period: UnitValue) -> None:
        try:
            min_temperature.validate_of_class("temperature")
            max_temperature.validate_of_class("temperature")
            min_radius.validate_of_class("length")
            max_radius.validate_of_class("length")
            min_density.validate_of_class("density")
            max_density.validate_of_class("density")
            min_rot_period.validate_of_class("time")
            max_rot_period.validate_of_class("time")
            min_orb_period.validate_of_class("time")
            max_orb_period.validate_of_class("time")
        except ValueError as e:
            raise ValueError(f"An error occured while initializing planet type: {e}")
        
        self.min_temperature = min_temperature
        self.max_temperature = max_temperature
        self.min_radius = min_radius
        self.max_radius = max_radius
        self.min_density = min_density
        self.max_density = max_density
        self.min_rot_period = min_rot_period
        self.max_rot_period = max_rot_period
        self.min_orb_period = min_orb_period
        self.max_orb_period = max_orb_period
        
    @staticmethod
    def from_dict(data: dict) -> 'PlanetType':
        temperature = data.get("temperature", None)
        radius = data.get("radius", None)
        density = data.get("density", None)
        rot_period = data.get("rotational_period", None)
        orb_period = data.get("orbital_period", None)

        min_temperature, max_temperature = PlanetType.get_min_max(temperature, 0)
        min_radius, max_radius = PlanetType.get_min_max(radius, 0)
        min_density, max_density = PlanetType.get_min_max(density, 0)
        min_rot_period, max_rot_period = PlanetType.get_min_max(rot_period, 0)
        min_orb_period, max_orb_period = PlanetType.get_min_max(orb_period, 0)

        planet_type = PlanetType(
            min_temperature=UnitValue(min_temperature, CONFIG.CONFIG_UNITS["temperature"]),
            max_temperature=UnitValue(max_temperature, CONFIG.CONFIG_UNITS["temperature"]),
            min_radius=UnitValue(min_radius, CONFIG.CONFIG_UNITS["length"]),
            max_radius=UnitValue(max_radius, CONFIG.CONFIG_UNITS["length"]),
            min_density=UnitValue(min_density, CONFIG.CONFIG_UNITS["density"]),
            max_density=UnitValue(max_density, CONFIG.CONFIG_UNITS["density"]),
            min_rot_period=UnitValue(min_rot_period, CONFIG.CONFIG_UNITS["time"]),
            max_rot_period=UnitValue(max_rot_period, CONFIG.CONFIG_UNITS["time"]),
            min_orb_period=UnitValue(min_orb_period, CONFIG.CONFIG_UNITS["time"]),
            max_orb_period=UnitValue(max_orb_period, CONFIG.CONFIG_UNITS["time"])
        )

        return planet_type

    @staticmethod
    def create(type_name: str) -> 'PlanetType':
        file_path = os.path.join(CURRENT_DIR, '..', 'data', 'planet_types', f'{type_name}.json')
        
        try:
            type_dict = file_to_dict(file_path=file_path)
        except FileNotFoundError:
            raise ValueError(f"Planet type {type_name} does not exist.")
        
        return PlanetType.from_dict(data=type_dict)
    
    @staticmethod
    def get_min_max(property_dict: Optional[dict], default = None) -> tuple:
        if property_dict is None:
            return default, default
        property_min = property_dict.get("min", default)
        property_max = property_dict.get("max", default)
        return property_min, property_max
    
    def generate_planetary_data(self) -> dict[str, UnitValue]:
        data = {
            "temperature": self.generate_temperature(),
            "radius": self.generate_radius(),
            "density": self.generate_density(),
            "rot_period": self.generate_rotational_period(),
            "orb_period": self.generate_orbital_period()
        }
        return data
        
    def generate_temperature(self) -> UnitValue:
        random_temperature = random.uniform(self.min_temperature.value, self.max_temperature.value)
        return UnitValue(random_temperature, CONFIG.CONFIG_UNITS["temperature"])
    
    def generate_radius(self) -> UnitValue:
        random_radius = random.uniform(self.min_radius.value, self.max_radius.value)
        return UnitValue(random_radius, CONFIG.CONFIG_UNITS["length"])
    
    def generate_density(self) -> UnitValue:
        random_density = random.uniform(self.min_density.value, self.max_density.value)
        return UnitValue(random_density, CONFIG.CONFIG_UNITS["density"])
    
    def generate_rotational_period(self) -> UnitValue:
        random_rot_period = random.uniform(self.min_rot_period.value, self.max_rot_period.value)
        return UnitValue(random_rot_period, CONFIG.CONFIG_UNITS["time"])
    
    def generate_orbital_period(self) -> UnitValue:
        random_orb_period = random.uniform(self.min_orb_period.value, self.max_orb_period.value)
        return UnitValue(random_orb_period, CONFIG.CONFIG_UNITS["time"])