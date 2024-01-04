import random
import src.modules.physics as phy
from src.planet_generation.planet_type import PlanetType
from src.planet_generation.unit_value import UnitValue

class Planet():
    def __init__(self, temperature: UnitValue, radius: UnitValue, density: UnitValue, rot_period: UnitValue, orb_period: UnitValue) -> None:
        temperature.validate_of_class("temperature")
        radius.validate_of_class("length")
        density.validate_of_class("density")
        rot_period.validate_of_class("time")
        orb_period.validate_of_class("time")

        self.temperature = temperature
        self.radius = radius
        self.density = density
        self.rot_period = rot_period
        self.orb_period = orb_period
        self.mass = phy.sphere_mass(radius=radius, density=density)
        self.volume = phy.sphere_volume(radius=radius)

        self.mass.validate_of_class("mass")
        self.volume.validate_of_class("volume")

    def __str__(self) -> str:
        metrics = [
            f"Temperature: {str(self.temperature)}",
            f"Radius: {str(self.radius)}",
            f"Volume: {str(self.volume)}",
            f"Density: {str(self.density)}",
            f"Mass: {str(self.mass)}",
            f"Rotational period: {str(self.rot_period)}",
            f"Orbital period: {str(self.orb_period)}"
        ]
        string = "\n".join(metrics)
        return string
        
    @staticmethod
    def from_dict(data: dict) -> 'Planet':
        retrieved_data = {
            "temperature": data.get("temperature", UnitValue.from_zero("temperature")),
            "radius": data.get("radius", UnitValue.from_zero("length")),
            "density": data.get("density", UnitValue.from_zero("density")),
            "rot_period": data.get("rot_period", UnitValue.from_zero("time")),
            "orb_period": data.get("orb_period", UnitValue.from_zero("time"))
        }

        for key, value in retrieved_data.items():
            if not isinstance(value, UnitValue):
                try:
                    retrieved_data[key] = UnitValue.from_any(value)
                except (ValueError, TypeError) as e:
                    raise ValueError(f"An error occured while trying to process {key} {value}: {e}")

        return Planet(**retrieved_data)
    
    def get_data(self) -> list[tuple]:
        data = [
            ("Temperature", str(self.temperature)),
            ("Radius", str(self.radius)),
            ("Volume", str(self.volume)),
            ("Density", str(self.density)),
            ("Mass", str(self.mass)),
            ("Rotational period", str(self.rot_period)),
            ("Orbital period", str(self.orb_period))
        ]
        return data
    
    def get_temperature(self) -> UnitValue:
        return self.temperature
    
    def get_radius(self) -> UnitValue:
        return self.radius
    
    def get_density(self) -> UnitValue:
        return self.density
    
    def get_rotational_period(self) -> UnitValue:
        return self.rot_period
    
    def get_orbital_period(self) -> UnitValue:
        return self.orb_period
    
    def get_mass(self) -> UnitValue:
        return self.mass
    
    def get_volume(self) -> UnitValue:
        return self.volume

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