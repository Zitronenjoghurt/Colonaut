import random
from src.molecule_database.molecule_database import MoleculeDatabase

MDB = MoleculeDatabase.get_instance()

class Atmosphere():
    def __init__(
            self,
            composition: list[tuple[str, float]]
        ) -> None:
        self.composition = composition

    def __str__(self) -> str:
        return "\n".join(f"{molecule}: {concentration}%" for molecule, concentration in self.composition)

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
 
def random_atmposphere(min_mass: float) -> Atmosphere:
    molecule_count = random.randint(5, 8)

    composition = MDB.generate_composition(molecule_count=molecule_count, min_molecular_mass=min_mass)

    atmosphere = Atmosphere(
        composition=composition
    )

    return atmosphere