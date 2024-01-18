import pytest
from src.utils.range import Range

list_data = [-200, 500]
dict_data = {"min": -200, "max": 500}

@pytest.fixture
def range():
    from_list = Range.create(data=list_data)
    from_dict = Range.create(data=dict_data)
    assert from_list == from_dict
    return from_list

def test_is_in_range(range: Range):
    assert range.is_in_range(-500) == False
    assert range.is_in_range(-200) == True
    assert range.is_in_range(-200, inclusive=False) == False
    assert range.is_in_range(300) == True
    assert range.is_in_range(300, inclusive=False) == True
    assert range.is_in_range(500) == True
    assert range.is_in_range(500, inclusive=False) == False

def test_get_difference(range: Range):
    assert range.get_difference() == 700

def test_get_distance_to(range: Range):
    assert range.get_distance_to(100) == 0
    assert range.get_distance_to(-200) == 0
    assert range.get_distance_to(600) == 100
    assert range.get_distance_to(-500) == 300

def test_get_relative_distance_to(range: Range):
    assert range.get_relative_distance_to(500) == 0
    assert range.get_relative_distance_to(1200) == 1
    assert range.get_relative_distance_to(1900) == 2
    assert range.get_relative_distance_to(-900) == 1
    assert range.get_relative_distance_to(-1600) == 2