import os
import src.modules.validator as validator
from ..constants.physical_units import EXISTING_CLASSES
from ..modules.utilities import file_to_dict

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE_PATH = os.path.join(CURRENT_DIR, '..', 'config.json')

class Config():
    _instance = None

    def __init__(self) -> None:
        if Config._instance is not None:
            raise RuntimeError("Tried to initialize multiple instances of Config.")
        
        config_data = file_to_dict(CONFIG_FILE_PATH)

        self.DECIMAL_DIGITS: int = config_data.get("decimal_digits", 2)
        self.SCIENTIFIC_NOTATION_UPPER_TRESHOLD: float = config_data.get("scientific_notation_upper_treshold", 1e7)
        self.SCIENTIFIC_NOTATION_LOWER_TRESHOLD: float = config_data.get("scientific_notation_lower_treshold", 1e-2)
        self.CONFIG_UNITS: dict[str, str] = config_data.get("config_units", {})
        self.DISPLAY_UNITS: dict[str, str] = config_data.get("display_units", {})
        self.DISPLAY_UNITS_CONVENIENTLY: list[str] = config_data.get("display_units_conveniently", [])

        try:
            validator.validate_int(self.DECIMAL_DIGITS, "decimal_digits", 0, 10)
            for unit_class in EXISTING_CLASSES:
                validator.validate_physical_unit_and_class(self.CONFIG_UNITS[unit_class], unit_class)
                validator.validate_physical_unit_and_class(self.DISPLAY_UNITS[unit_class], unit_class)
        except (ValueError, TypeError, KeyError) as e:
            raise RuntimeError(f"An error occured while initializing the config: {e}\nCheck your config at {CONFIG_FILE_PATH}")

    @staticmethod
    def get_instance() -> 'Config':
        if Config._instance is None:
            Config._instance = Config()
        return Config._instance