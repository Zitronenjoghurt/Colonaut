import os
import pytest
from src.classes.event import Event
from src.classes.event_bus import EventBus
from src.classes.response import Response
from src.classes.space_ship import SpaceShip
from src.classes.ship_system import ShipSystem
from src.classes.ship_systems import BatterySystem, HullSystem, SolarPanelSystem

from src.modules.utilities import file_to_dict

@pytest.fixture
def setup():
    EventBus.reset_instance()

@pytest.fixture
def current_dir():
    return os.path.dirname(os.path.abspath(__file__))

@pytest.fixture
def space_ship(setup, current_dir):
    ship_file = os.path.join(current_dir, '..', 'src', 'data', 'testing', 'ship.json')
    ship_dict = file_to_dict(ship_file)
    return SpaceShip.from_dict(data=ship_dict)

def assert_response_data(response: Response, expected_data):
    assert response.get_data() == expected_data

def test_default(setup):
    system = ShipSystem(max_hp=100)

    assert_response_data(system.get_name(), "default")
    assert_response_data(system.get_hp(), 100)
    assert_response_data(system.get_max_hp(), 100)

def test_damage(setup):
    system = ShipSystem(max_hp=100)

    with pytest.raises(ValueError) as exc:
        system.damage("bob") # type: ignore
    assert str(exc.value) == "amount must be of type int."

    with pytest.raises(ValueError) as exc:
        system.damage(-10)
    assert str(exc.value) == "amount must be greater or equal 0."

    system.damage(10)
    assert_response_data(system.get_hp(), 90)
    assert_response_data(system.get_max_hp(), 100)

def test_hull(space_ship: SpaceShip):
    hull: HullSystem = space_ship.get_system("hull").get_data()

    assert_response_data(hull.get_hp(), 100)
    assert_response_data(hull.get_max_hp(), 100)
    assert_response_data(hull.to_dict(), {"hp": 100, "max_hp": 100})

def test_battery(space_ship: SpaceShip):
    battery: BatterySystem = space_ship.get_system("battery").get_data()

    assert_response_data(battery.get_hp(), 100)
    assert_response_data(battery.get_max_hp(), 100)
    assert_response_data(battery.get_max_capacity(), 500)
    assert_response_data(battery.get_capacity(), 400)
    assert_response_data(battery.to_dict(), {"hp": 100, "max_hp": 100, "capacity": 400, "max_capacity": 500})

    # Charge
    with pytest.raises(ValueError) as exc:
        battery.charge("bob") # type: ignore
    assert str(exc.value) == "amount must be of type int."

    with pytest.raises(ValueError) as exc:
        battery.damage(-10)
    assert str(exc.value) == "amount must be greater or equal 0."

    battery.charge(amount=10)
    assert_response_data(battery.get_capacity(), 410)

    battery.publish_event(Event(Event.TYPES.BATTERY_CHARGE, amount = 10))
    assert_response_data(battery.get_capacity(), 420)

def test_solar_panel(space_ship: SpaceShip):
    solar_panel: SolarPanelSystem = space_ship.get_system("solar panel").get_data()

    assert_response_data(solar_panel.get_hp(), 100)
    assert_response_data(solar_panel.get_max_hp(), 100)
    assert_response_data(solar_panel.get_charge_capacity(), 20)

    # Solar panel charging battery
    battery: BatterySystem = space_ship.get_system("battery").get_data()
    assert_response_data(battery.get_capacity(), 400)

    response = solar_panel.work()
    assert response.get_message() == "Battery charged by 20"
    assert_response_data(battery.get_capacity(), 420)