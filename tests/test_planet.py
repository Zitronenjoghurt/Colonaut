import os
import pytest
from src.planet_generation.planet import Planet
from src.utils.file_operations import file_to_dict

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

@pytest.fixture
def planet():
    planet_file = os.path.join(CURRENT_DIR, '..', 'src', 'data', 'testing', 'planet.json')
    planet_dict = file_to_dict(planet_file)
    return Planet.from_dict(data=planet_dict)

def test_init(planet: Planet):
    temperature = planet.get_temperature()
    radius = planet.get_radius()
    density = planet.get_density()
    rot_period = planet.get_rotational_period()
    orb_period = planet.get_orbital_period()

    assert temperature.get_value() == 10
    assert radius.get_value() == 6000
    assert density.get_value() == 3000
    assert rot_period.get_value() == 20
    assert orb_period.get_value() == 5

    assert temperature.get_unit() == "°K"
    assert radius.get_unit() == "km"
    assert density.get_unit() == "kg/m^3"
    assert rot_period.get_unit() == "min"
    assert orb_period.get_unit() == "d"