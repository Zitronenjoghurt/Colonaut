import pytest
from src.space_ship.upgrade_model import UpgradeModel, UpgradeModelLibrary

@pytest.fixture
def model_library() -> UpgradeModelLibrary:
    return UpgradeModelLibrary.get_instance()

@pytest.fixture
def battery_model(model_library: UpgradeModelLibrary) -> UpgradeModel:
    return  model_library.get_model("battery")

def test_model(battery_model: UpgradeModel):
    assert battery_model.get_initial_value("max_capacity") == 100
    assert battery_model.get_level_value("max_capacity", 2) == 150
    assert battery_model.get_level_cost("max_capacity", 2) == 50
    assert battery_model.get_level_value("max_capacity", 3) == 200
    assert battery_model.get_level_cost("max_capacity", 3) == 100
    assert battery_model.get_level_value("max_capacity", 4) == 300
    assert battery_model.get_level_cost("max_capacity", 4) == 175

    assert battery_model.get_upgrade_difference("max_capacity", 1) == 50
    assert battery_model.get_upgrade_difference("max_capacity", 2) == 50
    assert battery_model.get_upgrade_difference("max_capacity", 3) == 100