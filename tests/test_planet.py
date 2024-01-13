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

    assert temperature.get_value() == 10
    assert radius.get_value() == 6000
    assert density.get_value() == 3000
    assert rot_period.get_value() == 20

    assert temperature.get_unit() == "°K"
    assert radius.get_unit() == "km"
    assert density.get_unit() == "kg/m^3"
    assert rot_period.get_unit() == "min"

def test_get_properties(planet: Planet):
    properties = planet.get_properties()
    assert properties[0][0] == "temperature"
    assert properties[0][1] == "-263.15°C"
    assert properties[1][0] == "radius"
    assert properties[1][1] == "6000km"
    assert properties[2][0] == "density"
    assert properties[2][1] == "3g/cm^3"
    assert properties[3][0] == "axial_tilt"
    assert properties[3][1] == "0°"
    assert properties[4][0] == "rot_period"
    assert properties[4][1] == "20min"
    assert properties[5][0] == "orb_period"
    assert properties[5][1] == "0s"
    assert properties[6][0] == "mass"
    assert properties[6][1] == "0.45Earth"
    assert properties[7][0] == "volume"
    assert properties[7][1] == "9.05e+20m^3"

    properties = planet.get_properties(["temperature", "orb_period"])
    assert properties[0][0] == "temperature"
    assert properties[0][1] == "-263.15°C"
    assert properties[1][0] == "radius"
    assert len(properties[1][1]) == 12
    assert properties[2][0] == "density"
    assert len(properties[2][1]) == 12
    assert properties[3][0] == "axial_tilt"
    assert len(properties[3][1]) == 12
    assert properties[4][0] == "rot_period"
    assert len(properties[4][1]) == 12
    assert properties[5][0] == "orb_period"
    assert properties[5][1] == "0s"
    assert properties[6][0] == "mass"
    assert len(properties[6][1]) == 12
    assert properties[7][0] == "volume"
    assert len(properties[7][1]) == 12