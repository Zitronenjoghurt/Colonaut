from typing import Optional
from ..constants.physical_units import UNIT_CLASS_MAP, EXISTING_UNITS, EXISTING_CLASSES

def validate_int(value: int, value_name: str = "value", min_value: Optional[int] = None, max_value: Optional[int] = None):
    if not isinstance(value, int):
        raise ValueError(f"{value_name} must be of type int.")
    
    if min_value is not None:
        if value < min_value:
            raise ValueError(f"{value_name} must be greater or equal {min_value}.")
    if max_value is not None:
        if value > max_value:
            raise ValueError(f"{value_name} must be less or equal {max_value}.")
        
def validate_physical_unit(unit: str):
    if unit not in EXISTING_UNITS:
        raise ValueError(f"Unit {unit} does not exist.")
    
def validate_physical_unit_class(unit_class: str):
    if unit_class not in EXISTING_CLASSES:
        raise ValueError(f"Unit class {unit_class} does not exist.")
    
def validate_physical_unit_and_class(unit: str, unit_class: str):
    validate_physical_unit(unit=unit)
    validate_physical_unit_class(unit_class=unit_class)

    unit_of_class = UNIT_CLASS_MAP.get(unit) == unit_class
    if not unit_of_class:
        raise ValueError(f"{unit} is not of class {unit_class}")