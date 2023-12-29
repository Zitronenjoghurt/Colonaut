import pytest
from src.classes.planet_type import PlanetType

@pytest.fixture
def ice_type():
    return PlanetType.create("ice")