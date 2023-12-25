import os
import random
from typing import Optional
from ..modules.utilities import file_to_dict

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

class PlanetType():
    def __init__(self, min_temperature: float = 0, max_temperature: float = 0, min_radius: float = 0, max_radius: float = 0, min_density: float = 0, max_density: float = 0) -> None:
        # Temperature in °K
        self.min_temperature = min_temperature
        self.max_temperature = max_temperature
        # Radius in km
        self.min_radius = min_radius
        self.max_radius = max_radius
        # Density in kg/m^3
        self.min_density = min_density
        self.max_density = max_density

    @staticmethod
    def from_dict(data: dict) -> 'PlanetType':
        temperature = data.get("temperature", None)
        radius = data.get("radius", None)
        density = data.get("density", None)

        min_temperature, max_temperature = PlanetType.get_min_max(temperature, 0)
        min_radius, max_radius = PlanetType.get_min_max(radius, 0)
        min_density, max_density = PlanetType.get_min_max(density, 0)

        planet_type = PlanetType(
            min_temperature=min_temperature,
            max_temperature=max_temperature,
            min_radius=min_radius,
            max_radius=max_radius,
            min_density=min_density,
            max_density=max_density
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
        
    def generate_temperature(self) -> float:
        random_temperature = random.uniform(self.min_temperature, self.max_temperature)
        return round(random_temperature, 2)
    
    def generate_radius(self) -> float:
        random_radius = random.uniform(self.min_radius, self.max_radius)
        return round(random_radius, 2)
    
    def generate_density(self) -> float:
        random_density = random.uniform(self.min_density, self.max_density)
        return round(random_density, 2)