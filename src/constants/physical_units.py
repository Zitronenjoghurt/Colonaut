CLASS_UNIT_MAP = {
    "length": ["mm", "cm", "m", "km"],
    "volume": ["mm^3", "cm^3", "m^3", "km^3"],
    "mass": ["g", "kg", "t"],
    "density": ["g/cm^3", "kg/m^3"],
    "temperature": ["°K", "°C", "°F"],
    "time": ["s", "min", "h", "d", "y"]
}

EXISTING_CLASSES = [unit_class for unit_class in CLASS_UNIT_MAP.keys()]
EXISTING_UNITS = [unit for units in CLASS_UNIT_MAP.values() for unit in units]
UNIT_CLASS_MAP = {unit: unit_class for unit_class, units in CLASS_UNIT_MAP.items() for unit in units}

# Abstract conversion functions
def linear_conversion(factor):
    def convert(value):
        return value * factor
    return convert

# Teperature conversion
def celcius_to_fahrenheit(celcius):
    return celcius * 9 / 5 + 32

def celcius_to_kelvin(celcius):
    return celcius + 273.15

def fahrenheit_to_celcius(fahrenheit):
    return (fahrenheit - 32) * 5 / 9

def fahrenheit_to_kelvin(fahrenheit):
    return (fahrenheit - 32) * 5 / 9 + 273.15

def kelvin_to_celcius(kelvin):
    return kelvin - 273.15

def kelvin_to_fahrenheit(kelvin):
    return (kelvin - 273.15) * 9 / 5 + 32

CONVERSIONS = {
    "mm": {"cm": linear_conversion(1e-1), "m": linear_conversion(1e-3), "km": linear_conversion(1e-6)},
    "cm": {"mm": linear_conversion(10), "m": linear_conversion(1e-2), "km": linear_conversion(1e-5)},
    "m": {"mm": linear_conversion(1e3), "cm": linear_conversion(1e2), "km": linear_conversion(1e-3)},
    "km": {"mm": linear_conversion(1e6), "cm": linear_conversion(1e5), "m": linear_conversion(1e3)},
    "mm^3": {"cm^3": linear_conversion(1e-3), "m^3": linear_conversion(1e-9), "km^3": linear_conversion(1e-18)},
    "cm^3": {"mm^3": linear_conversion(1e3), "m^3": linear_conversion(1e-6), "km^3": linear_conversion(1e-15)},
    "m^3": {"mm^3": linear_conversion(1e9), "cm^3": linear_conversion(1e6), "km^3": linear_conversion(1e-9)},
    "km^3": {"mm^3": linear_conversion(1e18), "cm^3": linear_conversion(1e15), "m^3": linear_conversion(1e9)},
    "g": {"kg": linear_conversion(1e-3), "t": linear_conversion(1e-6)},
    "kg": {"g": linear_conversion(1e3), "t": linear_conversion(1e-3)},
    "t": {"g": linear_conversion(1e6), "kg": linear_conversion(1e3)},
    "g/cm^3": {"kg/m^3": linear_conversion(1e3)},
    "kg/m^3": {"g/cm^3": linear_conversion(1e-3)},
    "°K": {"°C": kelvin_to_celcius, "°F": kelvin_to_fahrenheit},
    "°C": {"°K": celcius_to_kelvin, "°F": celcius_to_fahrenheit},
    "°F": {"°K": fahrenheit_to_kelvin, "°C": fahrenheit_to_celcius},
    "s": {"min": linear_conversion(1/60), "h": linear_conversion(1/3600), "d": linear_conversion(1/86400), "y": linear_conversion(1/31557600)},
    "min": {"s": linear_conversion(60), "h": linear_conversion(1/60), "d": linear_conversion(1/1440), "y": linear_conversion(1/525960)},
    "h": {"s": linear_conversion(3600), "min": linear_conversion(60), "d": linear_conversion(1/24), "y": linear_conversion(1/8766)},
    "d": {"s": linear_conversion(86400), "min": linear_conversion(1440), "h": linear_conversion(24), "y": linear_conversion(1/365.25)},
    "y": {"s": linear_conversion(31557600), "min": linear_conversion(525960), "h": linear_conversion(8766), "d": linear_conversion(365.25)}
}