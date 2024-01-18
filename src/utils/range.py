from numbers import Number
from typing import Any

class Range():
    def __init__(self, min: int|float, max: int|float) -> None:
        if not isinstance(min, Number):
            raise ValueError("Provided minimum value is not a number")
        if not isinstance(max, Number):
            raise ValueError("Provided maximum value is not a number")
        if min > max:
            min, max = max, min

        self.min = min
        self.max = max

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Range):
            return False
        return self.min == other.min and self.min == other.min

    def __repr__(self) -> str:
        return f"Range(min={self.min}, max={self.max})"
    
    def __getitem__(self, index):
        if index == 0:
            return self.min
        elif index == 1:
           return self.max
        else:
          raise IndexError("Index out of range. Range object has only two elements: min and max.")
        
    @staticmethod
    def create(data: Any) -> 'Range':
        try:
            if isinstance(data, list):
                return Range.from_list(data=data)
            elif isinstance(data, dict):
                return Range.from_dict(data=data)
            else:
                raise ValueError("Provided data has to be one of these types: list or dict")
        except ValueError as e:
            raise ValueError(f"An error occured while creating range object: {e}")
    
    @staticmethod
    def from_list(data: list) -> 'Range':
        if not isinstance(data, list):
            raise ValueError("Provided data is not a list")
        if len(data) < 2:
            raise ValueError("Provided list has no enough entries (needs 2)")
        min = data[0]
        max = data[1]
        return Range(min=min, max=max)
    
    @staticmethod
    def from_dict(data: dict) -> 'Range':
        if not isinstance(data, dict):
            raise ValueError("Provided data is not a dictionary")
        min = data.get("min", None)
        max = data.get("max", None)

        if min is None:
            raise ValueError("Provided dictionary is missing key 'min'")
        if max is None:
            raise ValueError("Provided dictionary is missing key 'max'")
        return Range(min=min, max=max)
    
    def to_list(self) -> list:
        return [self.min, self.max]
    
    def to_dict(self) -> dict:
        data = {
            "min": self.min,
            "max": self.max
        }
        return data
    
    def is_in_range(self, value: int|float, inclusive: bool = True) -> bool:
        if not isinstance(value, Number):
            raise ValueError("Provided value is not a number")
        
        if inclusive:
            lower_boundary = value >= self.min
            upper_boundary = value <= self.max
        else:
            lower_boundary = value > self.min
            upper_boundary = value < self.max

        return lower_boundary and upper_boundary
    
    def get_difference(self) -> float:
        return self.max - self.min
    
    def get_distance_to(self, value: int|float) -> float:
        if not isinstance(value, Number):
            raise ValueError("Provided value is not a number")
        if self.is_in_range(value=value):
            return 0
        
        if value > self.max:
            distance = value - self.max
        else:
            distance = self.min - value

        return distance
    
    # Return a value representing how far away from the range the provided value is
    def get_relative_distance_to(self, value: int|float) -> float:
        distance = self.get_distance_to(value=value)

        difference = self.get_difference()
        relative_distance = abs(distance)/difference
        return relative_distance