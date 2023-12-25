import pytest
from src.classes.planet_type import PlanetType

RANDOM_TEST_RUNS = 10000

@pytest.fixture
def ice_type():
    return PlanetType.create("ice")

def test_init(ice_type: PlanetType):
    assert ice_type.min_temperature.value == 10
    assert ice_type.max_temperature.value == 270
    assert ice_type.min_temperature.unit == "K"
    assert ice_type.max_temperature.unit == "K"

    assert ice_type.min_radius.value == 1000
    assert ice_type.max_radius.value == 20000
    assert ice_type.min_radius.unit == "km"
    assert ice_type.max_radius.unit == "km"

    assert ice_type.min_density.value == 1000
    assert ice_type.max_density.value == 2500
    assert ice_type.min_density.unit == "kg/m^3"
    assert ice_type.max_density.unit == "kg/m^3"

def test_generate_temperature(ice_type: PlanetType):
    for _ in range(RANDOM_TEST_RUNS):
        temp = ice_type.generate_temperature()
        assert temp >= ice_type.min_temperature.value
        assert temp <= ice_type.max_temperature.value

def test_generate_radius(ice_type: PlanetType):
    for _ in range(RANDOM_TEST_RUNS):
        radius = ice_type.generate_radius()
        assert radius >= ice_type.min_radius.value
        assert radius <= ice_type.max_radius.value

def test_generate_density(ice_type: PlanetType):
    for _ in range(RANDOM_TEST_RUNS):
        density = ice_type.generate_density()
        assert density >= ice_type.min_density.value
        assert density <= ice_type.max_density.value