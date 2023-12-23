import os
import pytest
from src.classes.space_ship import SpaceShip
from src.modules.utilities import file_to_dict

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

@pytest.fixture
def space_ship():
    ship_file = os.path.join(CURRENT_DIR, '..', 'src', 'data', 'testing', 'ship.json')
    ship_dict = file_to_dict(ship_file)
    return SpaceShip.from_dict(data=ship_dict)

def test_init(space_ship: SpaceShip):
    hull = space_ship.get_system("hull").get_data()
    assert hull.get_max_hitpoints() == 100