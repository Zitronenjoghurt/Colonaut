import src.modules.validator as validator
from .config import Config
from ..constants.physical_units import CONVERSIONS, UNIT_CLASS_MAP

CONFIG = Config.get_instance()

class UnitValue():
    def __init__(self, value: int|float, unit: str) -> None:
        validator.validate_physical_unit(unit=unit)

        self.value = float(value)
        self.unit = unit

    def __str__(self) -> str:
        return f"{str(self.get_value())}{self.unit}"
    
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
    
    def to_volume(self) -> 'UnitValue':
        self.validate_of_class("length")

        new_value = self.value ** 3
        new_unit = self.unit + "^3"

        return UnitValue(value=new_value, unit=new_unit)

    def get_value(self) -> float:
        return round(self.value, CONFIG.DECIMAL_DIGITS)
    
    def get_unit(self) -> str:
        return self.unit