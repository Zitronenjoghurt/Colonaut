from typing import Optional

def validate_int(value: int, value_name: str = "value", min_value: Optional[int] = None, max_value: Optional[int] = None):
    if not isinstance(value, int):
        raise ValueError(f"{value_name} must be of type int.")
    
    if min_value is not None:
        if value < min_value:
            raise ValueError(f"{value_name} must be greater or equal {min_value}.")
    if max_value is not None:
        if value > max_value:
            raise ValueError(f"{value_name} must be less or equal {max_value}.")