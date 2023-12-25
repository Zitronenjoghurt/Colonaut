import os
import src.modules.validator as validator
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
        self.DEFAULT_CONFIG_TEMPERATURE_UNIT: str = config_data.get("default_config_temperature_unit", "°K")
        self.DEFAULT_CONFIG_DENSITY_UNIT: str = config_data.get("default_config_density_unit", "kg/m^3")
        self.DEFAULT_CONFIG_LENGTH_UNIT: str = config_data.get("default_config_length_unit", "km")
        self.DISPLAY_TEMPERATURE_UNIT: str = config_data.get("display_temperature_unit", "°C")
        self.DISPLAY_DENSITY_UNIT: str = config_data.get("display_density_unit", "g/cm^3")
        self.DISPLAY_LENGTH_UNIT: str = config_data.get("display_length_unit", "km")

        try:
            validator.validate_int(self.DECIMAL_DIGITS, "decimal_digits", 0, 10)
            validator.validate_physical_unit_and_class(self.DEFAULT_CONFIG_TEMPERATURE_UNIT, "temperature")
            validator.validate_physical_unit_and_class(self.DEFAULT_CONFIG_DENSITY_UNIT, "density")
            validator.validate_physical_unit_and_class(self.DEFAULT_CONFIG_LENGTH_UNIT, "length")
            validator.validate_physical_unit_and_class(self.DISPLAY_TEMPERATURE_UNIT, "temperature")
            validator.validate_physical_unit_and_class(self.DISPLAY_DENSITY_UNIT, "density")
            validator.validate_physical_unit_and_class(self.DISPLAY_LENGTH_UNIT, "length")
        except ValueError as e:
            raise RuntimeError(f"An error occured while initializing the config: {e}\nCheck your config at {CONFIG_FILE_PATH}")

    @staticmethod
    def get_instance() -> 'Config':
        if Config._instance is None:
            Config._instance = Config()
        return Config._instance