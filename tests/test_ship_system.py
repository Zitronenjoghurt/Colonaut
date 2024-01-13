import os
import pytest
import src.space_ship.ship_systems as ShipSystems
from src.events.event import Event
from src.events.event_bus import EventBus
from src.events.response import Response
from src.space_ship.space_ship import SpaceShip
from src.space_ship.ship_system import ShipSystem
from src.utils.file_operations import file_to_dict

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

def assert_response_data(response: Response, expected_data, response_type = None):
    assert response.get_data(response_type=response_type) == expected_data

def test_hull(space_ship: SpaceShip):
    hull: ShipSystems.HullSystem = space_ship.get_system("hull").get_data()

    assert_response_data(hull.get_hp(), 100)
    assert_response_data(hull.get_max_hp(), 100)
    assert_response_data(hull.to_dict(), {"hp": 100, "max_hp": 100, 'levels': {'max_hp': 1}, 'model': 'standard', 'power_usage': 0})

def test_battery(space_ship: SpaceShip):
    battery: ShipSystems.BatterySystem = space_ship.get_system("battery").get_data()

    assert_response_data(battery.get_hp(), 100)
    assert_response_data(battery.get_max_hp(), 100)
    assert_response_data(battery.get_max_capacity(), 100)
    assert_response_data(battery.get_capacity(), 50)
    assert_response_data(battery.to_dict(), {"hp": 100, "max_hp": 100, "capacity": 50, "max_capacity": 100, 'levels': {'max_hp': 1, 'max_capacity': 1}, 'model': 'standard', 'power_usage': 0})

    # Charge
    with pytest.raises(ValueError) as exc:
        battery.charge("bob") # type: ignore
    assert str(exc.value) == "amount must be of type int"

    with pytest.raises(ValueError) as exc:
        battery.damage(-10)
    assert str(exc.value) == "amount must be greater or equal 0"

    battery.charge(amount=10)
    assert_response_data(battery.get_capacity(), 60)

    battery.publish_event(Event(Event.TYPES.BATTERY_CHARGE, amount = 10))
    assert_response_data(battery.get_capacity(), 70)

def test_solar_panel(space_ship: SpaceShip):
    solar_panel: ShipSystems.SolarPanelSystem = space_ship.get_system("solar_panel").get_data()

    assert_response_data(solar_panel.get_hp(), 100)
    assert_response_data(solar_panel.get_max_hp(), 100)
    assert_response_data(solar_panel.get_charge_capacity(), 20)

    # Solar panel charging battery
    battery: ShipSystems.BatterySystem = space_ship.get_system("battery").get_data()
    assert_response_data(battery.get_capacity(), 50)

    response = solar_panel.work()
    assert response.get_data(Response.TYPES.SHIP_STATUS_LOG_ENTRY)[0].texts == ["Solar panels collected 20 energy units"]
    assert response.get_data(Response.TYPES.SHIP_STATUS_LOG_ENTRY)[1].texts == ["Battery charged by 20"]
    assert_response_data(battery.get_capacity(), 70)

def test_sensors(space_ship: SpaceShip):
    accelerometer: ShipSystems.Accelerometer = space_ship.get_system("accelerometer").get_data()
    infrared_spectrometer: ShipSystems.InfraredSpectrometer = space_ship.get_system("infrared_spectrometer").get_data()
    laser_altimeter: ShipSystems.LaserAltimeter = space_ship.get_system("laser_altimeter").get_data()
    neutron_densitometer: ShipSystems.NeutronDensitometer = space_ship.get_system("neutron_densitometer").get_data()
    radio_telemetry: ShipSystems.RadioTelemetry = space_ship.get_system("radio_telemetry").get_data()

    assert_response_data(accelerometer.get_revealed_data(), ["mass", "star_mass", "escape_velocity", "gravity"])
    assert_response_data(infrared_spectrometer.get_revealed_data(), ["temperature"])
    assert_response_data(laser_altimeter.get_revealed_data(), ["radius", "volume", "axial_tilt"])
    assert_response_data(neutron_densitometer.get_revealed_data(), ["density"])
    assert_response_data(radio_telemetry.get_revealed_data(), ["orb_period", "rot_period", "distance_to_star"])

def test_scanner_results(space_ship: SpaceShip):
    space_ship.run()
    assert set(space_ship.scanner_results) == set(['mass', 'star_mass', 'temperature', 'radius', 'volume', 'axial_tilt', 'density', 'orb_period', 'rot_period', 'distance_to_star', 'esi', 'escape_velocity', 'gravity'])

    accelerometer: ShipSystems.Accelerometer = space_ship.get_system("accelerometer").get_data()
    accelerometer.reveal_chance = 0

    space_ship.run()
    assert set(space_ship.scanner_results) == set(["temperature", "radius", "volume", "axial_tilt", "density", "orb_period", "rot_period", "distance_to_star"])