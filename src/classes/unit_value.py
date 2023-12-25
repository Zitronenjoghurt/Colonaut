import math
import re
import src.modules.validator as validator
from .config import Config
from ..constants.physical_units import CONVERSIONS, UNIT_CLASS_MAP, CLASS_UNIT_MAP

CONFIG = Config.get_instance()

class UnitValue():
    def __init__(self, value: int|float, unit: str) -> None:
        validator.validate_physical_unit(unit=unit)

        self.value = float(value)
        self.unit = unit

    def __str__(self) -> str:
        unit_class = UNIT_CLASS_MAP.get(self.unit, "")
        if unit_class in CONFIG.DISPLAY_UNITS_CONVENIENTLY:
            converted_value = self.convert_conveniently()
        else:
            converted_value = self.convert(CONFIG.DISPLAY_UNITS[unit_class])
        return f"{str(converted_value.get_value_formatted())}{converted_value.get_unit()}"
    
    @staticmethod
    def from_zero(unit_class: str) -> 'UnitValue':
        validator.validate_physical_unit_class(unit_class=unit_class)
        class_units = CLASS_UNIT_MAP.get(unit_class, None)

        if class_units is None:
            raise RuntimeError(f"An error occured while retrieving available units of class {unit_class}")

        return UnitValue(0, class_units[0])
    
    @staticmethod
    def from_any(data) -> 'UnitValue':
        if isinstance(data, str):
            return UnitValue.from_string(data)
        if isinstance(data, dict):
            return UnitValue.from_dict(data)
        raise ValueError(f"Cant initialize unit value from given data: {data}")
    
    @staticmethod
    def from_string(string: str) -> 'UnitValue':
        match_groups = re.match(r"([0-9.e+-]+)([a-zA-Z/^]+[a-zA-Z0-9/^]*)", string)
        if match_groups:
            value = float(match_groups.group(1))
            unit = match_groups.group(2)
            return UnitValue(value=value, unit=unit)
        else:
            raise ValueError(f"Cant initialize unit value from string: invalid format.")
        
    @staticmethod
    def from_dict(data: dict) -> 'UnitValue':
        value = data.get("value", None)
        unit = data.get("unit", None)

        if value is None:
            raise ValueError(f"Cant initialize unit value from dict: no value given.")
        if unit is None:
            raise ValueError(f"Cant initialize unit value from dict: no value given.")
        
        try:
            value = float(value)
        except (ValueError, TypeError):
            raise ValueError(f"Cant initialize unit value from dict: value cant be converted to float")
        
        return UnitValue(value=value, unit=unit)
    
    def validate_of_class(self, unit_class: str) -> None:
        validator.validate_physical_unit_class(unit_class=unit_class)
        if not UNIT_CLASS_MAP.get(self.unit) == unit_class:
            raise ValueError(f"{self.unit} is not of class {unit_class}")

    def convert(self, target_unit: str) -> 'UnitValue':
        if self.unit == target_unit:
            return self
        validator.validate_physical_unit(unit=target_unit)

        self_unit_class = UNIT_CLASS_MAP.get(self.unit, None)
        target_unit_class = UNIT_CLASS_MAP.get(target_unit, None)

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
    
    def convert_conveniently(self) -> 'UnitValue':
        unit_class = UNIT_CLASS_MAP.get(self.unit, "")
        units = CLASS_UNIT_MAP.get(unit_class, [])

        unit_conversions = {}
        for unit in units:
            unit_conversions[unit] = self.convert(unit)

        most_convenient_unit = self.unit
        smallest_value_above_one = float('inf')
        for unit, unit_value in unit_conversions.items():
            value = unit_value.value
            if value >= 1 and value < smallest_value_above_one:
                smallest_value_above_one = value
                most_convenient_unit = unit

        return unit_conversions[most_convenient_unit]
    
    def to_volume(self) -> 'UnitValue':
        self.validate_of_class("length")

        new_value = self.value ** 3
        new_unit = self.unit + "^3"

        return UnitValue(value=new_value, unit=new_unit)

    def get_value(self) -> float:
        return self.value
    
    def get_value_formatted(self) -> str:
        use_scientific_notation = (abs(self.value) >= CONFIG.SCIENTIFIC_NOTATION_UPPER_TRESHOLD or abs(self.value) < CONFIG.SCIENTIFIC_NOTATION_LOWER_TRESHOLD) and self.value != 0
        if use_scientific_notation:
            return f"{self.value:.{CONFIG.DECIMAL_DIGITS}e}"
        else:
            return f"{self.value:.{CONFIG.DECIMAL_DIGITS}f}"
    
    def get_unit(self) -> str:
        return self.unit