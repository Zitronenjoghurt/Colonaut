import src.modules.physics as phy

CLASS_UNIT_MAP = {
    "length": ["mm", "cm", "m", "km"],
    "mass": ["g", "kg", "t"],
    "density": ["g/cm^3", "kg/m^3"],
    "temperature": ["°K", "°C", "°F"]
}

EXISTING_CLASSES = [unit_class for unit_class in CLASS_UNIT_MAP.keys()]
EXISTING_UNITS = [unit for units in CLASS_UNIT_MAP.values() for unit in units]
UNIT_CLASS_MAP = {unit: unit_class for unit_class, units in CLASS_UNIT_MAP.items() for unit in units}

# Conversion functions
def linear_conversion(factor):
    def convert(value):
        return value * factor
    return convert

CONVERSIONS = {
    "mm": {"cm": linear_conversion(0.1), "m": linear_conversion(0.001), "km": linear_conversion(0.000001)},
    "cm": {"mm": linear_conversion(10), "m": linear_conversion(0.01), "km": linear_conversion(0.00001)},
    "m": {"mm": linear_conversion(1000), "cm": linear_conversion(100), "km": linear_conversion(0.001)},
    "km": {"mm": linear_conversion(1000000), "cm": linear_conversion(100000), "m": linear_conversion(1000)},
    "g": {"kg": linear_conversion(0.001), "t": linear_conversion(0.000001)},
    "kg": {"g": linear_conversion(1000), "t": linear_conversion(0.001)},
    "t": {"g": linear_conversion(1000000), "kg": linear_conversion(1000)},
    "g/cm^3": {"kg/m^3": linear_conversion(1000)},
    "kg/m^3": {"g/cm^3": linear_conversion(0.001)},
    "°K": {"°C": phy.kelvin_to_celcius, "°F": phy.kelvin_to_fahrenheit},
    "°C": {"°K": phy.celcius_to_kelvin, "°F": phy.celcius_to_fahrenheit},
    "°F": {"°K": phy.fahrenheit_to_kelvin, "°C": phy.fahrenheit_to_celcius}
}