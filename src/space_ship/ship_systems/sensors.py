from src.space_ship.ship_system import SensorShipSystem

class Accelerometer(SensorShipSystem):
    NAME = "accelerometer"
    REVEALED_DATA = ["mass"]

class InfraredSpectrometer(SensorShipSystem):
    NAME = "infrared_spectrometer"
    REVEALED_DATA = ["temperature"]

class LaserAltimeter(SensorShipSystem):
    NAME = "laser_altimeter"
    REVEALED_DATA = ["radius", "volume"]

class NeutronDensitometer(SensorShipSystem):
    NAME = "neutron_densitometer"
    REVEALED_DATA = ["density"]

class RadioTelemetry(SensorShipSystem):
    NAME = "radio_telemetry"
    REVEALED_DATA = ["orb_period", "rot_period", "distance_to_star"]