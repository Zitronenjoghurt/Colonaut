import pytest
from src.molecule_database.aggregate_states import AggregateState
from src.molecule_database.molecule import Molecule
from src.planet_generation.unit_value import UnitValue

@pytest.fixture
def water():
    data = {
        "name": "water",
        "symbol": "H20",
        "melting_point": "0°C",
        "boiling_point": "100°C",
        "exist_weight": 100,
        "concentration_weight": {"min": 100, "max": 200}
    }
    return Molecule.from_dict(data=data)

def test_init(water: Molecule):
    assert water.get_name() == "water"
    assert water.get_symbol() == "H20"
    assert water.get_melting_point().convert("°C").get_value() == 0
    assert water.get_boiling_point().convert("°C").get_value() == 100
    assert water.get_exist_weight() == 100
    concentration_weight = water.get_concentration_weight()
    assert concentration_weight >= 100 and concentration_weight <= 200

def test_get_state_at(water: Molecule):
    solid_temp = UnitValue(-2, "°C")
    liquid_temp = UnitValue(20, "°C")
    gaseous_temp = UnitValue(120, "°C")

    assert water.get_state_at(solid_temp) == AggregateState.SOLID
    assert water.get_state_at(liquid_temp) == AggregateState.LIQUID
    assert water.get_state_at(gaseous_temp) == AggregateState.GASEOUS