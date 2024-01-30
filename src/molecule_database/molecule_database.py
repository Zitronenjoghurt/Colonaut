import numpy
from typing import Optional
from src.constants.config import Config
from src.constants.locale_translator import LocaleTranslator
from src.molecule_database.aggregate_states import AggregateState
from src.molecule_database.molecule import Molecule
from src.planet_generation.unit_value import UnitValue
from src.utils.file_operations import construct_path, file_to_dict
from src.utils.validator import validate_of_type

CONFIG = Config.get_instance()
LT = LocaleTranslator.get_instance()
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

        self.all_molecule_names = list(self.molecules_by_name.keys())
        self.total_molecule_count = len(self.all_molecule_names)

        all_exist_weights = self.get_exist_weights(self.all_molecule_names)
        sum_all_exist_weights = sum(all_exist_weights)
        self.exist_probabilities = [weight/sum_all_exist_weights for weight in all_exist_weights]

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
    
    def get_molecules(self, names_or_symbols: list[str]) -> list[Molecule]:
        return [self.get_molecule(name_or_symbol=name_or_symbol) for name_or_symbol in names_or_symbols]
    
    def get_molecules_with_state(self, state: AggregateState, temperature: UnitValue, molecule_names: Optional[list[str]] = None) -> list[str]:
        validate_of_type(state, AggregateState, "state")
        temperature.validate_of_class("temperature")

        if molecule_names is None:
            names_or_symbols = self.all_molecule_names
        else:
            names_or_symbols = molecule_names
        
        result = []
        for name_or_symbol in names_or_symbols:
            molecule = self.get_molecule(name_or_symbol=name_or_symbol)
            if molecule.get_state_at(temperature=temperature) == state:
                result.append(molecule.get_name())
        return result
    
    def get_molecules_with_mass_above(self, mass: float) -> list[str]:
        i = 0
        names = list(self.name_to_mass.keys())
        masses = list(self.name_to_mass.values())

        while i < len(masses) and masses[i] <= mass:
            i+=1
        
        return names[i:]
    
    def get_molecules_with_mass_above_and_state(self, mass: float, state: AggregateState, temperature: UnitValue) -> list[str]:
        validate_of_type(state, AggregateState, "state")
        temperature.validate_of_class("temperature")

        molecule_names = self.get_molecules_with_mass_above(mass=mass)

        result = self.get_molecules_with_state(state=state, temperature=temperature, molecule_names=molecule_names)
        return result
    
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
    
    def contains_radioactive_molecule(self, molecule_names: list[str]) -> bool:
        for molecule_name in molecule_names:
            molecule = self.get_molecule(molecule_name)
            if molecule.is_radioactive():
                return True
        return False
    
    def check_composition_breathability(self, composition: list[tuple[str, float]], temperature: Optional[UnitValue] = None) -> tuple[float, str]:
        # Check temperature before everything else
        if isinstance(temperature, UnitValue):
            temperature.validate_of_class("temperature")
            temp = temperature.convert("°C").get_value()
            if temp < -30:
                return 0, LT.get(LT.KEYS.BREATHABILITY_TOO_COLD)
            if temp > 50:
                return 0, LT.get(LT.KEYS.BREATHABILITY_TOO_HOT)

        names = [entry[0] for entry in composition]
        concentrations = [entry[1] for entry in composition]

        molecules = self.get_molecules(names_or_symbols=names)

        if "oxygen" not in names:
            return 0, LT.get(LT.KEYS.BREATHABILITY_NO_OXYGEN)
        
        lethal_gases = []
        for i, molecule in enumerate(molecules):
            lethal_concentration = molecule.get_lethal_concentration()
            if not lethal_concentration:
                continue
            lethal_concentration = lethal_concentration.convert("%").get_value()
            if concentrations[i] >= lethal_concentration:
                lethal_gases.append(names[i])

        if len(lethal_gases) != 0:
            message = LT.get(LT.KEYS.BREATHABILITY_LETHAL_GASES) + " " + ", ".join([LT.get(name) for name in lethal_gases])
            return 0, message
        
        ideal_oxygen_percentage = 21.0
        oxygen_index = names.index("oxygen")
        oxygen_percentage = concentrations[oxygen_index]

        deviation = abs(oxygen_percentage - ideal_oxygen_percentage)

        max_deviation = 10.0
        breathability = max(0, 100 - (deviation / max_deviation * 100))

        if oxygen_percentage > ideal_oxygen_percentage + max_deviation:
            return 0, LT.get(LT.KEYS.BREATHABILITY_OXYGEN_TOO_HIGH)
        if oxygen_percentage < ideal_oxygen_percentage - max_deviation:
            return 0, LT.get(LT.KEYS.BREATHABILITY_OXYGEN_TOO_LOW)

        return breathability, LT.get(LT.KEYS.BREATHABILITY_PERCENTAGE).format(breathability=breathability)
    
    def select_random_molecules(self, count: int) -> list[str]:
        if count > self.total_molecule_count or count < 0:
            raise ValueError(f"Molecule count can only be between 1 and {self.total_molecule_count}")
        return list(numpy.random.choice(self.all_molecule_names, size=count, replace=False, p=self.exist_probabilities))
    
    def generate_composition(self, molecule_count: int, min_molecular_mass: float, temperature: Optional[UnitValue] = None) -> list[tuple[str, float]]:
        if molecule_count > self.total_molecule_count:
            raise ValueError(f"Tried to generate a composition with {molecule_count} molecules, but the database only includes {self.total_molecule_count}")
        if molecule_count < 0:
            raise ValueError(f"Molecule count has to be greater than 0.")
        if temperature is not None:
            temperature.validate_of_class("temperature")
        
        selected_molecules = self.select_random_molecules(count=molecule_count)

        # Filter the selected molecules based on if they are above the min molecular mass and gaseous at the given temperature
        final_molecules = []
        for molecule_name in selected_molecules:
            molecule = self.get_molecule(molecule_name)
            if molecule.get_atomic_mass().get_value() >= min_molecular_mass:
                if temperature is None or molecule.get_state_at(temperature=temperature) == AggregateState.GASEOUS:
                    final_molecules.append(molecule.get_name())

        concentration_weights = self.get_concentration_weights(final_molecules)
        total_concentration_weight = sum(concentration_weights)

        composition = []
        for name, concentration in zip(final_molecules, concentration_weights):
            concentration = round(concentration/total_concentration_weight*100, CONFIG.DECIMAL_DIGITS)
            composition.append((name, concentration))
        
        return sorted(composition, key=lambda x: x[1], reverse=True)