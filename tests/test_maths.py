from src.utils.maths import clam, linear_interpolation

def test_clam():
    assert clam(10, 0, 10) == 10
    assert clam(10, 0, 5) == 5
    assert clam(-10000, 0, 1) == 0

def test_linear_interpolation():
    assert linear_interpolation(0, 100, 0) == 0
    assert linear_interpolation(0, 100, 0.5) == 50
    assert linear_interpolation(0, 100, 1) == 100
    assert linear_interpolation(-100, -5000, 0.5) == -2550