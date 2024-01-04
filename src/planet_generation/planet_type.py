from src.constants.config import Config
from src.planet_generation.probability import Probability
from src.planet_generation.unit_value import UnitValue
from src.utils.file_operations import file_to_dict

CONFIG = Config.get_instance()

class PlanetType():
    def __init__(self, 
                 random_temperature: Probability, 
                 random_radius: Probability, 
                 random_density: Probability, 
                 random_rot_period: Probability,
                 random_orb_period: Probability) -> None:
        self.random_temperature = random_temperature
        self.random_radius = random_radius
        self.random_density = random_density
        self.random_rot_period = random_rot_period
        self.random_orb_period = random_orb_period
        
    @staticmethod
    def from_dict(data: dict) -> 'PlanetType':
        temperature = data.get("temperature", None)
        radius = data.get("radius", None)
        density = data.get("density", None)
        rot_period = data.get("rotational_period", None)
        orb_period = data.get("orbital_period", None)

        planet_type = PlanetType(
            random_temperature = Probability.create(temperature),
            random_radius = Probability.create(radius),
            random_density = Probability.create(density),
            random_rot_period = Probability.create(rot_period),
            random_orb_period = Probability.create(orb_period)
        )

        return planet_type

    @staticmethod
    def create(type_name: str) -> 'PlanetType':
        file_path = CONFIG.PLANET_TYPES_FILE_PATH.format(type_name=type_name)
        
        try:
            type_dict = file_to_dict(file_path=file_path)
        except FileNotFoundError:
            raise ValueError(f"Planet type {type_name} does not exist.")
        
        return PlanetType.from_dict(data=type_dict)
    
    def generate_planetary_data(self) -> dict[str, UnitValue]:
        data = {
            "temperature": UnitValue(self.random_temperature.generate(), CONFIG.CONFIG_UNITS["temperature"]),
            "radius": UnitValue(self.random_radius.generate(), CONFIG.CONFIG_UNITS["length"]),
            "density": UnitValue(self.random_density.generate(), CONFIG.CONFIG_UNITS["density"]),
            "rot_period": UnitValue(self.random_rot_period.generate(), CONFIG.CONFIG_UNITS["time"]),
            "orb_period": UnitValue(self.random_orb_period.generate(), CONFIG.CONFIG_UNITS["time"])
        }
        return data