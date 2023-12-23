import os
import pytest
from src.classes.event import Event
from src.classes.event_bus import EventBus
from src.classes.space_ship import SpaceShip
from src.classes.ship_system import ShipSystem, HullSystem
from src.modules.utilities import file_to_dict

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

@pytest.fixture
def setup():
    EventBus.reset_instance()

@pytest.fixture
def space_ship(setup):
    ship_file = os.path.join(CURRENT_DIR, '..', 'src', 'data', 'testing', 'ship.json')
    ship_dict = file_to_dict(ship_file)
    return SpaceShip.from_dict(data=ship_dict)

def test_default(setup):
    system = ShipSystem(max_hitpoints=100)

    assert system.get_name() == "default"
    assert system.get_hitpoints() == 100
    assert system.get_max_hitpoints() == 100

def test_damage(setup):
    system = ShipSystem(max_hitpoints=100)

    with pytest.raises(ValueError) as exc:
        system.damage("bob") # type: ignore
    assert str(exc.value) == "Amount must be of type int."

    with pytest.raises(ValueError) as exc:
        system.damage(-10) # type: ignore
    assert str(exc.value) == "Amount must be greater or equal 0."

    system.damage(10)
    assert system.get_hitpoints() == 90
    assert system.get_max_hitpoints() == 100

def test_hull(space_ship: SpaceShip):
    hull: HullSystem = space_ship.get_system("hull").get_data()

    assert hull.get_hitpoints() == 100
    assert hull.get_max_hitpoints() == 100

    assert hull.to_dict() == {"hitpoints": 100, "max_hitpoints": 100}