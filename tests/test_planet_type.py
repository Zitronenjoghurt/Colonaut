import pytest
from src.classes.planet_type import PlanetType

RANDOM_TEST_RUNS = 10000

@pytest.fixture
def ice_type():
    return PlanetType.create("ice")

def test_init(ice_type: PlanetType):
    assert ice_type.min_temperature == 10
    assert ice_type.max_temperature == 270
    assert ice_type.min_radius == 1000
    assert ice_type.max_radius == 20000
    assert ice_type.min_density == 1000
    assert ice_type.max_density == 2500

def test_generate_temperature(ice_type: PlanetType):
    for _ in range(RANDOM_TEST_RUNS):
        temp = ice_type.generate_temperature()
        assert temp >= ice_type.min_temperature
        assert temp <= ice_type.max_temperature

def test_generate_radius(ice_type: PlanetType):
    for _ in range(RANDOM_TEST_RUNS):
        radius = ice_type.generate_radius()
        assert radius >= ice_type.min_radius
        assert radius <= ice_type.max_radius

def test_generate_density(ice_type: PlanetType):
    for _ in range(RANDOM_TEST_RUNS):
        density = ice_type.generate_density()
        assert density >= ice_type.min_density
        assert density <= ice_type.max_density