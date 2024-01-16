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