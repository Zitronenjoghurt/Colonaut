from src.molecule_database.aggregate_states import AggregateState
from src.molecule_database.molecule import Molecule
from src.utils.file_operations import construct_path, file_to_dict

MOLECULES_FILE_PATH = construct_path("src/data/molecules.json")

class MoleculeDatabase():
    _instance = None
    
    def __init__(self) -> None:
        if MoleculeDatabase._instance is not None:
            raise RuntimeError("Tried to initialize multiple instances of MoleculeDatabase.")
        self.molecules_by_name = {}
        self.molecules_by_symbol = {}

        # Will be sorted ascending depending on the molecules mass
        self.name_to_mass = {}

        self._load_molecules()
        self._sort_by_mass()

    def _load_molecules(self) -> None:
        data = file_to_dict(MOLECULES_FILE_PATH)

        for molecule_name, molecule_data in data.items():
            molecule_data["name"] = molecule_name
            try:
                molecule = Molecule.from_dict(molecule_data)
            except ValueError as e:
                raise RuntimeError(f"An error occured while initializing molecule database: {e}")
            self.molecules_by_name[molecule_name.lower()] = molecule
            self.molecules_by_symbol[molecule.get_symbol().lower()] = molecule
            self.name_to_mass[molecule_name.lower()] = molecule.get_atomic_mass().convert("u").get_value()

    def _sort_by_mass(self) -> None:
        sorted_molecules = sorted(self.name_to_mass.items(), key=lambda molecule: molecule[1])
        self.name_to_mass = dict(sorted_molecules)
        
    @staticmethod
    def get_instance() -> 'MoleculeDatabase':
        if MoleculeDatabase._instance is None:
            MoleculeDatabase._instance = MoleculeDatabase()
        return MoleculeDatabase._instance
    
    def get_molecule(self, name_or_symbol: str) -> Molecule:
        name_or_symbol = name_or_symbol.lower()
        if name_or_symbol in self.molecules_by_name:
            return self.molecules_by_name[name_or_symbol]
        if name_or_symbol in self.molecules_by_symbol:
            return self.molecules_by_symbol[name_or_symbol]
        raise ValueError(f"Molecule with name or symbol {name_or_symbol} does not exist in current molecule database.")
    
    def get_molecules_with_mass_above(self, mass: float) -> list[str]:
        i = 0
        names = list(self.name_to_mass.keys())
        masses = list(self.name_to_mass.values())

        while i < len(masses) and masses[i] <= mass:
            i+=1
        
        return names[i:]
    
    def get_molecules_with_mass_below(self, mass: float) -> list[str]:
        i = 0
        names = list(self.name_to_mass.keys())
        masses = list(self.name_to_mass.values())

        while i < len(masses):
            if masses[i] > mass:
                break
            i += 1
        
        return names[:i]