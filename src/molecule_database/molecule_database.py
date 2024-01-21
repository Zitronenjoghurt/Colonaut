from src.molecule_database.element import Element
from src.utils.file_operations import construct_path, file_to_dict

ELEMENTS_FILE_PATH = construct_path("src/data/elements.json")

class MoleculeDatabase():
    _instance = None
    
    def __init__(self) -> None:
        if MoleculeDatabase._instance is not None:
            raise RuntimeError("Tried to initialize multiple instances of MoleculeDatabase.")
        self.elements = {}
        self._load_elements()

    def _load_elements(self) -> None:
        data = file_to_dict(ELEMENTS_FILE_PATH)

        for element_name, element_data in data.items():
            element_data["name"] = element_name
            try:
                element = Element.from_dict(element_data)
            except ValueError as e:
                raise RuntimeError(f"An error occured while initializing molecule database: {e}")
            self.elements[element_name] = element
        
    @staticmethod
    def get_instance() -> 'MoleculeDatabase':
        if MoleculeDatabase._instance is None:
            MoleculeDatabase._instance = MoleculeDatabase()
        return MoleculeDatabase._instance