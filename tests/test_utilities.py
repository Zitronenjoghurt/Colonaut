import os
import pytest
from src.modules.utilities import file_to_dict

@pytest.fixture
def current_dir():
    return os.path.dirname(os.path.abspath(__file__))

def test_file_to_dict(current_dir):
    test_file = os.path.join(current_dir, '..', 'src', 'data', 'testing', 'dict.json')
    data = file_to_dict(file_path=test_file)

    assert data["foo"] == "bar"
    assert data["hello"][0] == "world"