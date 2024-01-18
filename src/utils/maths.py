from numbers import Number

def clam(value: int|float, min: int|float, max: int|float) -> int|float:
    if not isinstance(value, Number):
        raise ValueError("Provided value is not a number.")
    if not isinstance(min, Number):
        raise ValueError("Provided minimum is not a number.")
    if not isinstance(max, Number):
        raise ValueError("Provided maximum is not a number.")
    
    if value > max:
        value = max
    elif value < min:
        value = min
    
    return value

def linear_interpolation(value1: int|float, value2: int|float, progress: float) -> float:
    if not isinstance(value1, Number):
        raise ValueError("The first proivided value is not a number.")
    if not isinstance(value2, Number):
        raise ValueError("The second proivided value is not a number.")
    if progress < 0 or progress > 1:
        raise ValueError("Progress factor can only be between 0 and 1.")
    return value1 + (value2 - value1) * progress