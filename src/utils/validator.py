from typing import Optional
from ..constants.physical_units import UNIT_CLASS_MAP, EXISTING_UNITS, EXISTING_CLASSES
from ..ui.style_tags import StyleTags

def validate_int(value: int, value_name: str = "value", min_value: Optional[int] = None, max_value: Optional[int] = None):
    validate_of_type(value, int, value_name)
    
    if min_value is not None:
        if value < min_value:
            raise ValueError(f"{value_name} must be greater or equal {min_value}")
    if max_value is not None:
        if value > max_value:
            raise ValueError(f"{value_name} must be less or equal {max_value}")
        
def validate_of_type(value: int, required_type: type, value_name: str = "value"):
    if not isinstance(value, required_type):
        raise ValueError(f"{value_name} must be of type {required_type.__name__}")
        
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
    
def validate_style_tag(style_tag: str):
    for tag in StyleTags.TAGS:
        tag_name = tag.get("tagName")
        if not tag_name:
            raise ValueError("An error occured while validating the configured style tag: a tag is missing the tagName property")
        if style_tag == tag_name:
            return
    raise ValueError(f"Style tag {style_tag} does not exist.")