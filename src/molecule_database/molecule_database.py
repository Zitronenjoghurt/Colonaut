import numpy
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
    
    def molecule_exists(self, name_or_symbol: str) -> bool:
        name_or_symbol = name_or_symbol.lower()
        return name_or_symbol in self.molecules_by_name or name_or_symbol in self.molecules_by_symbol
    
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
    
    def get_exist_weights(self, molecule_names: list[str]) -> list[int]:
        weights = []
        for molecule_name in molecule_names:
            if self.molecule_exists(molecule_name):
                molecule = self.get_molecule(molecule_name)
                weights.append(molecule.get_exist_weight())
            else:
                weights.append(0)
        return weights
    
    def get_concentration_weights(self, molecule_names: list[str]) -> list[int]:
        weights = []
        for molecule_name in molecule_names:
            if self.molecule_exists(molecule_name):
                molecule = self.get_molecule(molecule_name)
                weights.append(molecule.get_concentration_weight())
            else:
                weights.append(0)
        return weights
    
    def generate_composition(self, molecule_count: int, min_molecular_mass: float) -> list[tuple[str, float]]:
        molecule_names = self.get_molecules_with_mass_above(min_molecular_mass)
        exist_weights = self.get_exist_weights(molecule_names)

        if molecule_count < len(molecule_names) and molecule_count > 0:
            total_weight = sum(exist_weights)
            probabilities = [weight/total_weight for weight in exist_weights]
            selected_molecules = list(numpy.random.choice(molecule_names, size=molecule_count, replace=False, p=probabilities))
        else:
            selected_molecules = molecule_names

        concentration_weights = self.get_concentration_weights(selected_molecules)
        total_concentration_weight = sum(concentration_weights)

        composition = []
        for name, concentration in zip(selected_molecules, concentration_weights):
            composition.append((name, concentration/total_concentration_weight*100))
        
        return composition