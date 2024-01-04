import pytest
from src.planet_generation.planet_type import PlanetType

@pytest.fixture
def ice_type():
    return PlanetType.create("ice")