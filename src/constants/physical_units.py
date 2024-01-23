CLASS_UNIT_MAP = {
    "length": ["mm", "cm", "m", "km", "AU"],
    "volume": ["mm^3", "cm^3", "m^3", "km^3"],
    "mass": ["grm", "kg", "t", "Earth", "Sun"],
    "atomic_mass": ["u"],
    "density": ["g/cm^3", "kg/m^3"],
    "temperature": ["°K", "°C", "°F"],
    "time": ["s", "min", "h", "d", "y"],
    "angle": ["°"],
    "acceleration": ["m/s^2", "g"],
    "speed": ["km/h", "m/s", "km/s"]
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
    "mm": {"cm": linear_conversion(1e-1), "m": linear_conversion(1e-3), "km": linear_conversion(1e-6), "AU": linear_conversion(1/1.496e14)},
    "cm": {"mm": linear_conversion(10), "m": linear_conversion(1e-2), "km": linear_conversion(1e-5), "AU": linear_conversion(1/1.496e13)},
    "m": {"mm": linear_conversion(1e3), "cm": linear_conversion(1e2), "km": linear_conversion(1e-3), "AU": linear_conversion(1/1.496e11)},
    "km": {"mm": linear_conversion(1e6), "cm": linear_conversion(1e5), "m": linear_conversion(1e3), "AU": linear_conversion(1/1.496e8)},
    "AU": {"mm": linear_conversion(1.496e14), "cm": linear_conversion(1.496e13), "m": linear_conversion(1.496e11), "km": linear_conversion(1.496e8)},
    "mm^3": {"cm^3": linear_conversion(1e-3), "m^3": linear_conversion(1e-9), "km^3": linear_conversion(1e-18)},
    "cm^3": {"mm^3": linear_conversion(1e3), "m^3": linear_conversion(1e-6), "km^3": linear_conversion(1e-15)},
    "m^3": {"mm^3": linear_conversion(1e9), "cm^3": linear_conversion(1e6), "km^3": linear_conversion(1e-9)},
    "km^3": {"mm^3": linear_conversion(1e18), "cm^3": linear_conversion(1e15), "m^3": linear_conversion(1e9)},
    "grm": {"kg": linear_conversion(1e-3), "t": linear_conversion(1e-6), "Earth": linear_conversion(1/5.972e27), "Sun": linear_conversion(1/1.989e33)},
    "kg": {"grm": linear_conversion(1e3), "t": linear_conversion(1e-3), "Earth": linear_conversion(1/5.972e24), "Sun": linear_conversion(1/1.989e30)},
    "t": {"grm": linear_conversion(1e6), "kg": linear_conversion(1e3), "Earth": linear_conversion(1/5.972e21), "Sun": linear_conversion(1/1.989e27)},
    "Earth": {"grm": linear_conversion(5.972e27), "kg": linear_conversion(5.972e24), "t": linear_conversion(5.972e21), "Sun": linear_conversion(1/333000)},
    "Sun": {"grm": linear_conversion(1.989e33), "kg": linear_conversion(1.989e30), "t": linear_conversion(1.989e27), "Earth": linear_conversion(333000)},
    "g/cm^3": {"kg/m^3": linear_conversion(1e3)},
    "kg/m^3": {"g/cm^3": linear_conversion(1e-3)},
    "°K": {"°C": kelvin_to_celcius, "°F": kelvin_to_fahrenheit},
    "°C": {"°K": celcius_to_kelvin, "°F": celcius_to_fahrenheit},
    "°F": {"°K": fahrenheit_to_kelvin, "°C": fahrenheit_to_celcius},
    "s": {"min": linear_conversion(1/60), "h": linear_conversion(1/3600), "d": linear_conversion(1/86400), "y": linear_conversion(1/31557600)},
    "min": {"s": linear_conversion(60), "h": linear_conversion(1/60), "d": linear_conversion(1/1440), "y": linear_conversion(1/525960)},
    "h": {"s": linear_conversion(3600), "min": linear_conversion(60), "d": linear_conversion(1/24), "y": linear_conversion(1/8766)},
    "d": {"s": linear_conversion(86400), "min": linear_conversion(1440), "h": linear_conversion(24), "y": linear_conversion(1/365.25)},
    "y": {"s": linear_conversion(31557600), "min": linear_conversion(525960), "h": linear_conversion(8766), "d": linear_conversion(365.25)},
    "km/h": {"m/s": linear_conversion(1/3.6), "km/s": linear_conversion(1/3600)},
    "m/s": {"km/h": linear_conversion(3.6), "km/s": linear_conversion(1/1000)},
    "km/s": {"km/h": linear_conversion(3600), "m/s": linear_conversion(1000)},
    "m/s^2": {"g": linear_conversion(1/9.81)},
    "g": {"m/s^2": linear_conversion(9.81)}
}