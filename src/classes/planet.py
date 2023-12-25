import src.modules.physics as phy
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

        self.mass.validate_of_class("mass")
        
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