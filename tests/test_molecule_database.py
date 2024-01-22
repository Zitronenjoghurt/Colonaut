import pytest
from src.molecule_database.molecule import Molecule
from src.molecule_database.molecule_database import MoleculeDatabase

@pytest.fixture
def database():
    DB = MoleculeDatabase.get_instance()
    return DB

def test_init(database: MoleculeDatabase):
    for molecule in database.molecules_by_name.values():
        assert isinstance(molecule, Molecule)
    for molecule in database.molecules_by_symbol.values():
        assert isinstance(molecule, Molecule)
    
    assert set(database.molecules_by_name.keys()) == set([molecule.get_name().lower() for molecule in database.molecules_by_name.values()])
    assert set(database.molecules_by_name.keys()) == set([molecule.get_name().lower() for molecule in database.molecules_by_symbol.values()])
    assert set(database.molecules_by_symbol.keys()) == set([molecule.get_symbol().lower() for molecule in database.molecules_by_name.values()])
    assert set(database.molecules_by_symbol.keys()) == set([molecule.get_symbol().lower() for molecule in database.molecules_by_symbol.values()])

def test_get_molecule(database: MoleculeDatabase):
    hydrogens = [
        database.get_molecule("hydrogen"),
        database.get_molecule("Hydrogen"),
        database.get_molecule("h"),
        database.get_molecule("H")
    ]
    assert all(hydrogen is hydrogens[0] for hydrogen in hydrogens)