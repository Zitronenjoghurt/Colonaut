import src.modules.physics as phy

CLASS_UNITS = {
    "length": ["mm", "cm", "m", "km"],
    "mass": ["g", "kg", "t"],
    "density": ["g/cm^3", "kg/m^3"],
    "temperature": ["K", "C", "F"]
}

EXISTING_UNITS = [unit for units in CLASS_UNITS.values() for unit in units]
UNIT_CLASS = {unit: unit_class for unit_class, units in CLASS_UNITS.items() for unit in units}

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
    "K": {"C": phy.kelvin_to_celcius, "F": phy.kelvin_to_fahrenheit},
    "C": {"K": phy.celcius_to_kelvin, "F": phy.celcius_to_fahrenheit},
    "F": {"K": phy.fahrenheit_to_kelvin, "C": phy.fahrenheit_to_celcius}
}

class UnitValue():
    def __init__(self, value: int|float, unit: str) -> None:
        self.validate_unit(unit=unit)

        self.value = value
        self.unit = unit

    @staticmethod
    def validate_unit(unit: str) -> None:
        if unit not in EXISTING_UNITS:
            raise ValueError(f"Unit {unit} does not exist.")

    def convert(self, target_unit: str) -> 'UnitValue':
        if self.unit == target_unit:
            return self
        self.validate_unit(unit=target_unit)

        self_unit_class = UNIT_CLASS.get(self.unit, None)
        target_unit_class = UNIT_CLASS.get(target_unit, None)

        if not self_unit_class or not target_unit_class:
            raise ValueError("An error occured while retrieving the unit classes for conversion.")
        if self_unit_class != target_unit_class:
            raise ValueError(f"Cannot convert between {self_unit_class} and {target_unit_class}.")
        
        conversion_functions = CONVERSIONS.get(self.unit, None)
        if conversion_functions is None:
            raise ValueError(f"No conversion functions specified for {self.unit}")
        
        conversion_function = conversion_functions.get(target_unit, None)
        if conversion_function is None:
            raise ValueError(f"No function specified for conversion from {self.unit} to {target_unit}")
        
        new_value = conversion_function(self.value)
        return UnitValue(value=new_value, unit=target_unit)