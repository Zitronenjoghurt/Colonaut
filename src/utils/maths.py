from numbers import Number

def linear_interpolation(value1: int|float, value2: int|float, progress: float) -> float:
    if not isinstance(value1, Number):
        raise ValueError("The first proivided value is not a number.")
    if not isinstance(value2, Number):
        raise ValueError("The second proivided value is not a number.")
    if progress < 0 or progress > 1:
        raise ValueError("Progress factor can only be between 0 and 1.")
    return value1 + (value2 - value1) * progress