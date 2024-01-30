import random
from typing import Optional
from src.molecule_database.molecule_database import MoleculeDatabase
from src.planet_generation.unit_value import UnitValue

MDB = MoleculeDatabase.get_instance()

class Atmosphere():
    def __init__(
            self,
            composition: list[tuple[str, float]]
        ) -> None:
        self.composition = composition
        self.molecules = [entry[0] for entry in self.composition]
        self.radioactive = MDB.contains_radioactive_molecule(self.molecules)

    def __str__(self) -> str:
        return "\n".join(f"{molecule}: {concentration}%" for molecule, concentration in self.composition)
    
    @staticmethod
    def create_empty() -> 'Atmosphere':
        return Atmosphere([])

    @staticmethod
    def from_dict(data: dict) -> 'Atmosphere':
        composition_data = data.get("composition", [])
        composition = []
        for entry in composition_data:
            composition.append((entry[0], entry[1]))

        atmosphere = Atmosphere(
            composition=composition
        )

        return atmosphere

    def to_dict(self) -> dict:
        composition = []
        for entry in self.composition:
            composition.append([entry[0], entry[1]])

        data = {
            "composition": composition
        }

        return data
    
    def is_radioactive(self) -> bool:
        return self.radioactive
    
    def get_composition(self) -> list[tuple[str, str]]:
        composition = []
        for entry in self.composition:
            composition.append((entry[0], str(entry[1])+"%"))
        return composition
    
    def get_breathability(self, temperature: Optional[UnitValue] = None) -> tuple[float, str]:
        return MDB.check_composition_breathability(composition=self.composition, temperature=temperature)
 
def random_atmposphere(min_mass: float, temperature: Optional[UnitValue] = None) -> Atmosphere:
    molecule_count = random.randint(7, 12)

    composition = MDB.generate_composition(molecule_count=molecule_count, min_molecular_mass=min_mass, temperature=temperature)

    atmosphere = Atmosphere(
        composition=composition
    )

    return atmosphere