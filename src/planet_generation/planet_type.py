from src.constants.config import Config
from src.planet_generation.probability import Probability
from src.planet_generation.unit_value import UnitValue
from src.utils.file_operations import construct_path, file_to_dict
from src.utils import validator

CONFIG = Config.get_instance()
PLANET_TYPES_FILE_PATH = construct_path("src/data/planet_types/{type_name}.json")

PROPERTY_UNIT_CLASSES = {
    "temperature": "temperature",
    "radius": "length",
    "density": "density",
    "rot_period": "time",
    "distance_to_star": "length",
    "star_mass": "mass",
    "axial_tilt": "angle"
}

class PlanetType():
    LIBRARY = {}

    def __init__(self,
                 units: dict[str, str],
                 name: str,
                 random_temperature: Probability, 
                 random_radius: Probability, 
                 random_density: Probability, 
                 random_rot_period: Probability,
                 random_distance_to_star: Probability,
                 random_star_mass: Probability,
                 random_axial_tilt: Probability,
                 clouds: Probability) -> None:
        self.validate_units(units)
        self.units = units
        self.name = name
        self.random_temperature = random_temperature
        self.random_radius = random_radius
        self.random_density = random_density
        self.random_rot_period = random_rot_period
        self.random_distance_to_star = random_distance_to_star
        self.random_star_mass = random_star_mass
        self.random_axial_tilt = random_axial_tilt
        self.clouds = clouds

    @staticmethod
    def validate_units(units: dict[str, str]) -> None:
        for property, unit_class in PROPERTY_UNIT_CLASSES.items():
            if property not in units:
                raise ValueError(f"Unit for property {property} not specified")
            unit = units[property]
            validator.validate_physical_unit_and_class(unit=unit, unit_class=unit_class)
        
    @staticmethod
    def from_dict(data: dict) -> 'PlanetType':
        units = data.get("units", None)
        name = data.get("name", None)
        temperature = data.get("temperature", None)
        radius = data.get("radius", None)
        density = data.get("density", None)
        rot_period = data.get("rot_period", None)
        distance_to_star = data.get("distance_to_star", None)
        star_mass = data.get("star_mass", None)
        axial_tilt = data.get("axial_tilt", None)
        clouds = data.get("clouds", False)

        planet_type = PlanetType(
            units=units,
            name=name,
            random_temperature = Probability.create(temperature),
            random_radius = Probability.create(radius),
            random_density = Probability.create(density),
            random_rot_period = Probability.create(rot_period),
            random_distance_to_star=Probability.create(distance_to_star),
            random_star_mass=Probability.create(star_mass),
            random_axial_tilt=Probability.create(axial_tilt),
            clouds=Probability.create(clouds)
        )

        return planet_type

    @staticmethod
    def create(type_name: str) -> 'PlanetType':
        if type_name in PlanetType.LIBRARY:
            return PlanetType.LIBRARY[type_name]
        
        file_path = PLANET_TYPES_FILE_PATH.format(type_name=type_name)
        
        try:
            type_dict = file_to_dict(file_path=file_path)
        except FileNotFoundError:
            raise ValueError(f"Planet type {type_name} does not exist.")
        
        type_dict["name"] = type_name

        planet_type = PlanetType.from_dict(data=type_dict)
        PlanetType.LIBRARY[type_name] = planet_type
        return planet_type
    
    def get_unit(self, property: str) -> str:
        return self.units[property]
    
    def generate_planetary_data(self) -> dict:
        data = {
            "temperature": UnitValue(self.random_temperature.generate(), self.get_unit("temperature")),
            "radius": UnitValue(self.random_radius.generate(), self.get_unit("radius")),
            "density": UnitValue(self.random_density.generate(), self.get_unit("density")),
            "rot_period": UnitValue(self.random_rot_period.generate(), self.get_unit("rot_period")),
            "distance_to_star": UnitValue(self.random_distance_to_star.generate(), self.get_unit("distance_to_star")),
            "star_mass": UnitValue(self.random_star_mass.generate(), self.get_unit("star_mass")),
            "axial_tilt": UnitValue(self.random_axial_tilt.generate(), self.get_unit("axial_tilt")),
            "clouds": self.clouds.generate()
        }
        return data