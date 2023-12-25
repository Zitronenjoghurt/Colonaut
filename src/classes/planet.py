import random

import src.modules.physics as phy
from .planet_type import PlanetType
from .unit_value import UnitValue

class Planet():
    def __init__(self, temperature: UnitValue, radius: UnitValue, density: UnitValue) -> None:
        temperature.validate_of_class("temperature")
        radius.validate_of_class("length")
        density.validate_of_class("density")

        self.temperature = temperature
        self.radius = radius
        self.density = density
        self.mass = phy.sphere_mass(radius=radius, density=density)
        self.volume = phy.sphere_volume(radius=radius)

        self.mass.validate_of_class("mass")
        self.volume.validate_of_class("volume")

    def __str__(self) -> str:
        string = f"Temperature: {str(self.temperature)}\nRadius: {str(self.radius)}\nVolume: {str(self.volume)}\nDensity: {str(self.density)}\nMass: {str(self.mass)}"
        return string
        
    @staticmethod
    def from_dict(data: dict) -> 'Planet':
        retrieved_data = {
            "temperature": data.get("temperature", UnitValue.from_zero("temperature")),
            "radius": data.get("radius", UnitValue.from_zero("length")),
            "density": data.get("density", UnitValue.from_zero("density"))
        }

        for key, value in retrieved_data.items():
            if not isinstance(value, UnitValue):
                try:
                    retrieved_data[key] = UnitValue.from_any(value)
                except (ValueError, TypeError) as e:
                    raise ValueError(f"An error occured while trying to process {key} {value}: {e}")

        return Planet(**retrieved_data)
    
    def get_temperature(self) -> UnitValue:
        return self.temperature
    
    def get_radius(self) -> UnitValue:
        return self.radius
    
    def get_density(self) -> UnitValue:
        return self.density
    
    def get_mass(self) -> UnitValue:
        return self.mass

WEIGHTS = {
    "ice": 100
}
TOTAL_WEIGHT = sum(WEIGHTS.values())

class PlanetGenerator:
    @staticmethod
    def generate() -> Planet:
        type_name = PlanetGenerator.random_planet_type()
        planet_type = PlanetType.create(type_name=type_name)
        planet_data = planet_type.generate_planetary_data()
        return Planet.from_dict(data=planet_data)

    @staticmethod
    def random_planet_type() -> str:
        random_value = random.uniform(0, TOTAL_WEIGHT)
        for planet_type, weight in WEIGHTS.items():
            random_value -= weight
            if random_value <= 0:
                return planet_type
        raise RuntimeError("Planet type randomization did not yield any planet type.")