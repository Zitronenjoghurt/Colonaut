import os
import pytest
from src.classes.planet import Planet
from src.modules.utilities import file_to_dict

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

    assert temperature.get_value() == 10
    assert radius.get_value() == 6000
    assert density.get_value() == 3000

    assert temperature.get_unit() == "°K"
    assert radius.get_unit() == "km"
    assert density.get_unit() == "kg/m^3"