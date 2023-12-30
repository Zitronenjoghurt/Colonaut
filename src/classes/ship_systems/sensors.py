from src.classes.ship_system import SensorShipSystem

class Accelerometer(SensorShipSystem):
    NAME = "accelerometer"
    REVEALED_DATA = ["mass"]

class InfraredSpectrometer(SensorShipSystem):
    NAME = "infrared spectrometer"
    REVEALED_DATA = ["temperature"]

class LaserAltimeter(SensorShipSystem):
    NAME = "laser altimeter"
    REVEALED_DATA = ["radius"]

class NeutronDensitometer(SensorShipSystem):
    NAME = "neutron densitometer"
    REVEALED_DATA = ["density"]

class RadioTelemetry(SensorShipSystem):
    NAME = "radio telemetry"
    REVEALED_DATA = ["orb_period", "rot_period"]