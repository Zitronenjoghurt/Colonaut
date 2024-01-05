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

def test_get_properties(planet: Planet):
    properties = planet.get_properties()
    assert properties[0][0] == "Temperature"
    assert properties[0][1] == "-263.15°C"
    assert properties[1][0] == "Radius"
    assert properties[1][1] == "6000km"
    assert properties[2][0] == "Density"
    assert properties[2][1] == "3g/cm^3"
    assert properties[3][0] == "Rotational Period"
    assert properties[3][1] == "20min"
    assert properties[4][0] == "Orbital Period"
    assert properties[4][1] == "5d"
    assert properties[5][0] == "Mass"
    assert properties[5][1] == "2.71e+24kg"
    assert properties[6][0] == "Volume"
    assert properties[6][1] == "9.05e+20m^3"

    properties = planet.get_properties(["temperature", "orb_period"])
    assert properties[0][0] == "Temperature"
    assert properties[0][1] == "-263.15°C"
    assert properties[1][0] == "Radius"
    assert properties[1][1] == "??????????"
    assert properties[2][0] == "Density"
    assert properties[2][1] == "??????????"
    assert properties[3][0] == "Rotational Period"
    assert properties[3][1] == "??????????"
    assert properties[4][0] == "Orbital Period"
    assert properties[4][1] == "5d"
    assert properties[5][0] == "Mass"
    assert properties[5][1] == "??????????"
    assert properties[6][0] == "Volume"
    assert properties[6][1] == "??????????"