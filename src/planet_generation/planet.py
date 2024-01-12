import random
import src.utils.physics as phy
from typing import Optional
from src.constants.locale_translator import LocaleTranslator
from src.planet_generation.planet_image import PlanetImageLibrary, PlanetImage
from src.planet_generation.planet_type import PlanetType
from src.planet_generation.unit_value import UnitValue
from src.utils.gibberish import gibber
from src.utils.validator import validate_of_type

LT = LocaleTranslator.get_instance()
PLANET_IMAGE_LIBRARY = PlanetImageLibrary.get_instance()

class Planet():
    # Which properties will be shown in the data window
    DATA_PROPERTIES = ["temperature", "radius", "density", "rot_period", "orb_period", "mass", "volume", "distance_to_star"]

    def __init__(
            self, 
            temperature: UnitValue, 
            radius: UnitValue, 
            density: UnitValue, 
            rot_period: UnitValue,
            distance_to_star: UnitValue,
            star_mass: UnitValue,
            clouds: bool, 
            tags: list[str], 
            possible_tags: list[str],
            image: Optional[PlanetImage] = None
        ) -> None:
        temperature.validate_of_class("temperature")
        radius.validate_of_class("length")
        density.validate_of_class("density")
        rot_period.validate_of_class("time")
        distance_to_star.validate_of_class("length")
        star_mass.validate_of_class("mass")
        validate_of_type(clouds, bool)
        validate_of_type(tags, list)
        validate_of_type(possible_tags, list)

        self.temperature = temperature
        self.radius = radius
        self.density = density
        self.rot_period = rot_period
        self.orb_period = phy.orbital_period(distance_to_star=distance_to_star, mass_star=star_mass)
        self.distance_to_star = distance_to_star
        self.star_mass = star_mass
        self.clouds = clouds
        self.mass = phy.sphere_mass(radius=radius, density=density)
        self.volume = phy.sphere_volume(radius=radius)
        self.tags = tags
        
        for tag in possible_tags:
            self.handle_possible_tag(tag)

        if image is None:
            image = PLANET_IMAGE_LIBRARY.get_by_tags(self.tags)

        self.image: Optional[PlanetImage] = image

        self.orb_period.validate_of_class("time")
        self.mass.validate_of_class("mass")
        self.volume.validate_of_class("volume")

    def __str__(self) -> str:
        properties = self.get_properties()
        string = "\n".join([f"{property[0]}: {property[1]}" for property in properties])
        return string
    
    def handle_possible_tag(self, tag: str) -> None:
        match tag:
            case "clouds":
                if self.clouds:
                    self.tags.append(tag)
        
    @staticmethod
    def from_dict(data: dict, possible_tags: Optional[list[str]] = None) -> 'Planet':
        if possible_tags is None:
            possible_tags = []

        retrieved_data = {
            "temperature": data.get("temperature", UnitValue.from_zero("temperature")),
            "radius": data.get("radius", UnitValue.from_zero("length")),
            "density": data.get("density", UnitValue.from_zero("density")),
            "rot_period": data.get("rot_period", UnitValue.from_zero("time")),
            "distance_to_star": data.get("distance_to_star", UnitValue.from_zero("length")),
            "star_mass": data.get("star_mass", UnitValue.from_zero("mass")),
            "clouds": data.get("clouds", False),
            "tags": data.get("tags", [])
        }

        unit_values = ["temperature", "radius", "density", "rot_period", "distance_to_star", "star_mass"]
        for key, value in retrieved_data.items():
            if key in unit_values and not isinstance(value, UnitValue):
                try:
                    retrieved_data[key] = UnitValue.from_any(value)
                except (ValueError, TypeError) as e:
                    raise ValueError(f"An error occured while initializing planet, trying to transform key {key} with value {value} to UnitValue: {e}")
        
        image_data = data.get("image", None)
        if image_data:
            retrieved_data["image"] = PlanetImage.from_dict(image_data)
        retrieved_data["possible_tags"] = possible_tags

        return Planet(**retrieved_data)
    
    def to_dict(self) -> dict:
        image = self.image if not self.image else self.image.to_dict()

        data = {
            "temperature": str(self.temperature),
            "radius": str(self.radius),
            "density": str(self.density),
            "rot_period": str(self.rot_period),
            "orb_period": str(self.orb_period),
            "distance_to_star": str(self.distance_to_star),
            "star_mass": str(self.star_mass),
            "clouds": self.clouds,
            "tags": self.tags,
            "image": image
        }
        return data
    
    def get_properties(self, revealed_data: Optional[list[str]] = None) -> list[tuple[str, str]]:
        properties = []
        for property in self.DATA_PROPERTIES:
            if isinstance(revealed_data, list) and property not in revealed_data:
                value = gibber(12)
            else:
                value = getattr(self, property)
            property = (property, str(value))
            properties.append(property)
        return properties
    
    def get_report(self, revealed_data: Optional[list[str]] = None) -> dict:
        data = {
            "image": None if not self.image else self.image.get_ctk_image(200, 200)
        }
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

# Tags all planets of this type will get
REQUIRED_TAGS = {
    "ice": ["ice"]
}

# Tags all planets of this type CAN get depending on specific factors
POSSIBLE_TAGS = {
    "ice": ["clouds"]
}

class PlanetGenerator:
    @staticmethod
    def generate() -> Planet:
        type_name = PlanetGenerator.random_planet_type()
        planet_type = PlanetType.create(type_name=type_name)
        planet_data = planet_type.generate_planetary_data()

        planet_data["tags"] = REQUIRED_TAGS[type_name].copy()

        return Planet.from_dict(
            data=planet_data,
            possible_tags=POSSIBLE_TAGS[type_name].copy()
        )

    @staticmethod
    def random_planet_type() -> str:
        random_value = random.uniform(0, TOTAL_WEIGHT)
        for planet_type, weight in WEIGHTS.items():
            random_value -= weight
            if random_value <= 0:
                return planet_type
        raise RuntimeError("Planet type randomization did not yield any planet type.")