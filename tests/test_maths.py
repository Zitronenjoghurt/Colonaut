from src.utils.maths import linear_interpolation

def test_linear_interpolation():
    assert linear_interpolation(0, 100, 0) == 0
    assert linear_interpolation(0, 100, 0.5) == 50
    assert linear_interpolation(0, 100, 1) == 100
    assert linear_interpolation(-100, -5000, 0.5) == -2550