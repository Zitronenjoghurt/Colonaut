import os
import pytest
from src.classes.event import Event
from src.classes.event_bus import EventBus
from src.classes.space_ship import SpaceShip
from src.classes.ship_system import HullSystem
from src.modules.utilities import file_to_dict

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
@pytest.fixture
def space_ship():
    EventBus.reset_instance()
    ship_file = os.path.join(CURRENT_DIR, '..', 'src', 'data', 'testing', 'ship.json')
    ship_dict = file_to_dict(ship_file)
    return SpaceShip.from_dict(data=ship_dict)

def test_init(space_ship: SpaceShip):
    hull: HullSystem = space_ship.get_system("hull").get_data()
    assert hull.get_hp() == 100
    assert hull.get_max_hp() == 100

def test_damage_system(space_ship: SpaceShip):
    damage_event = Event(Event.TYPES.SHIP_DAMAGE_SYSTEM, system_name = "hull", amount = 10)
    space_ship.publish_event(event=damage_event)

    hull: HullSystem = space_ship.get_system("hull").get_data()
    assert hull.get_hp() == 90
    assert hull.get_max_hp() == 100