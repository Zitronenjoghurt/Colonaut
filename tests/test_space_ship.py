import os
import pytest
from src.events.event import Event
from src.events.event_bus import EventBus
from src.events.response import Response
from src.space_ship.space_ship import SpaceShip
from src.space_ship.ship_systems import HullSystem
from src.utils.file_operations import file_to_dict

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
@pytest.fixture
def space_ship():
    EventBus.reset_instance()
    ship_file = os.path.join(CURRENT_DIR, '..', 'src', 'data', 'testing', 'ship.json')
    ship_dict = file_to_dict(ship_file)
    return SpaceShip.from_dict(data=ship_dict)

def assert_response_data(response: Response, expected_data):
    assert response.get_data() == expected_data

def test_init(space_ship: SpaceShip):
    hull: HullSystem = space_ship.get_system("hull").get_data()
    assert_response_data(hull.get_hp(), 100)
    assert_response_data(hull.get_max_hp(), 100)

def test_damage_system(space_ship: SpaceShip):
    damage_event = Event(Event.TYPES.SHIP_DAMAGE_SYSTEM, system_name = "hull", amount = 10)
    space_ship.publish_event(event=damage_event)

    hull: HullSystem = space_ship.get_system("hull").get_data()
    assert_response_data(hull.get_hp(), 90)
    assert_response_data(hull.get_max_hp(), 100)