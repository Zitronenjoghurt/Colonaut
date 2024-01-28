import pytest
from src.molecule_database.aggregate_states import AggregateState
from src.molecule_database.molecule import Molecule
from src.molecule_database.molecule_database import MoleculeDatabase
from src.planet_generation.unit_value import UnitValue

@pytest.fixture
def database() -> MoleculeDatabase:
    DB = MoleculeDatabase.get_instance()
    return DB

@pytest.fixture
def hydrogen_molecule() -> Molecule:
    data = {
        "name": "hydrogen",
        "symbol": "H2",
        "atomic_mass": "2u",
        "melting_point": "13.99°K",
        "boiling_point": "20.271°K",
        "exist_weight": 250,
        "concentration_weight": {"min": 10, "max": 1000},
        "lethal_concentration": "20ppm"
    }
    return Molecule.from_dict(data=data)

@pytest.fixture
def helium_molecule() -> Molecule:
    data = {
        "name": "helium",
        "symbol": "He",
        "atomic_mass": "4u",
        "melting_point": "0.95°K",
        "boiling_point": "4.222°K",
        "exist_weight": 2000,
        "concentration_weight": {
            "weights": [100, 1],
            "values":[
                {"min": 10, "max": 50},
                {"min": 500, "max": 1000}
            ]
        }
    }
    return Molecule.from_dict(data=data)

def test_init(database: MoleculeDatabase):
    for molecule in database.molecules_by_name.values():
        assert isinstance(molecule, Molecule)
    for molecule in database.molecules_by_symbol.values():
        assert isinstance(molecule, Molecule)
    
    assert set(database.molecules_by_name.keys()) == set([molecule.get_name().lower() for molecule in database.molecules_by_name.values()])
    assert set(database.molecules_by_name.keys()) == set([molecule.get_name().lower() for molecule in database.molecules_by_symbol.values()])
    assert set(database.molecules_by_symbol.keys()) == set([molecule.get_symbol().lower() for molecule in database.molecules_by_name.values()])
    assert set(database.molecules_by_symbol.keys()) == set([molecule.get_symbol().lower() for molecule in database.molecules_by_symbol.values()])

def test_get_molecule(database: MoleculeDatabase, hydrogen_molecule: Molecule, helium_molecule: Molecule):
    hydrogens = [
        database.get_molecule("hydrogen"),
        database.get_molecule("Hydrogen"),
        database.get_molecule("h2"),
        database.get_molecule("H2")
    ]
    assert all(hydrogen == hydrogen_molecule for hydrogen in hydrogens)

    heliums = [
        database.get_molecule("helium"),
        database.get_molecule("Helium"),
        database.get_molecule("HE"),
        database.get_molecule("he")
    ]
    assert all(helium == helium_molecule for helium in heliums)

def test_molecule_exists(database: MoleculeDatabase):
    assert database.molecule_exists("hydrogen") == True
    assert database.molecule_exists("h2") == True
    assert database.molecule_exists("H2") == True
    assert database.molecule_exists("HYDROGEN") == True
    assert database.molecule_exists("hyDroGEN") == True
    assert database.molecule_exists("hydrobobs") == False

def test_get_molecules_with_state(database: MoleculeDatabase):
    iron_solid = UnitValue(1800, "°K")
    assert database.get_molecules_with_state(AggregateState.SOLID, iron_solid) == ["iron"]

    helium_gaseous = UnitValue(5, "°K")
    assert database.get_molecules_with_state(AggregateState.GASEOUS, helium_gaseous) == ["helium"]

def test_get_molecules_with_mass_above(database: MoleculeDatabase):
    assert database.get_molecules_with_mass_above(140) == ["sulfur_hexafluoride"]

def test_get_molecules_with_mass_above_and_state(database: MoleculeDatabase):
    hydrogen_helium_gaseous = UnitValue(21, "°K")
    assert database.get_molecules_with_mass_above_and_state(1, AggregateState.GASEOUS, hydrogen_helium_gaseous) == ["hydrogen", "helium"]
    assert database.get_molecules_with_mass_above_and_state(3, AggregateState.GASEOUS, hydrogen_helium_gaseous) == ["helium"]

def test_get_molecules_with_mass_below(database: MoleculeDatabase):
    assert database.get_molecules_with_mass_below(4.1) == ["hydrogen", "helium"]

def test_get_exist_weights(database: MoleculeDatabase):
    assert database.get_exist_weights(["hydrogen", "helium"]) == [250, 2000]