import pytest
from src.classes.planet_type import PlanetType

@pytest.fixture
def ice_type():
    return PlanetType.create("ice")

def test_init(ice_type: PlanetType):
    assert str(ice_type.random_temperature) == "(min:10-max:270)"
    assert str(ice_type.random_density) == "(min:1000-max:2500)"
    assert str(ice_type.random_radius) == "(min:1000-max:20000)"
    assert str(ice_type.random_rot_period) == "(min:1000-max:320000000.0)"
    assert str(ice_type.random_orb_period) == "(min:3000-max:31000000000.0)"