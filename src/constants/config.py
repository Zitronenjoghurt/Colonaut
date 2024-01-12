import src.utils.validator as validator
from src.constants.physical_units import EXISTING_CLASSES
from src.utils.file_operations import file_to_dict, construct_path

CONFIG_FILE_PATH = construct_path("src/config.json")

DEFAULT = {
    "file_paths": {
        "game_state": "src/",
        "global_state": "src/"
    },
    "save_file_mode": "cbor",
    "decimal_digits": 2,
    "scientific_notation_upper_treshhold": 1e7,
    "scientific_notation_lower_treshold": 1e-2,
    "display_units": {
        "temperature": "°C",
        "density": "g/cm^3",
        "length": "km",
        "mass": "kg",
        "volume": "m^3",
        "time": "h",
        "angle": "°"
    },
    "display_units_convenience_treshold": {
        "time": 1,
        "mass": 1e-2,
        "length": 1e-2
    },
    "default_ship_console_char_delay": 17,
    "default_ship_console_line_delay": 150,
    "default_ship_console_style_tag": "computer"
}

SAVE_FILE_MODES = ["json", "cbor"]

class Config():
    _instance = None

    def __init__(self) -> None:
        if Config._instance is not None:
            raise RuntimeError("Tried to initialize multiple instances of Config.")
        
        config_data = file_to_dict(CONFIG_FILE_PATH)

        self.DECIMAL_DIGITS: int = config_data.get("decimal_digits", DEFAULT["decimal_digits"])
        self.SCIENTIFIC_NOTATION_UPPER_TRESHOLD: float = config_data.get("scientific_notation_upper_treshold", DEFAULT["scientific_notation_upper_treshhold"])
        self.SCIENTIFIC_NOTATION_LOWER_TRESHOLD: float = config_data.get("scientific_notation_lower_treshold", DEFAULT["scientific_notation_lower_treshold"])
        self.DISPLAY_UNITS_CONVENIENCE_THRESHOLD: dict[str, int|float] = config_data.get("display_units_convenience_treshold", DEFAULT["display_units_convenience_treshold"])
        self.DEFAULT_SHIP_CONSOLE_CHAR_DELAY: int = config_data.get("default_ship_console_char_delay", DEFAULT["default_ship_console_char_delay"])
        self.DEFAULT_SHIP_CONSOLE_LINE_DELAY: int = config_data.get("default_ship_console_line_delay", DEFAULT["default_ship_console_line_delay"])
        self.DEFAULT_SHIP_CONSOLE_STYLE_TAG: str = config_data.get("default_ship_console_style_tag", DEFAULT["default_ship_console_style_tag"])
        
        self.SAVE_FILE_MODE: str = config_data.get("save_file_mode", DEFAULT["save_file_mode"])
        if self.SAVE_FILE_MODE not in SAVE_FILE_MODES:
            self.SAVE_FILE_MODE = DEFAULT["save_file_mode"]

        self.DISPLAY_UNITS: dict[str, str] = config_data.get("display_units", DEFAULT["display_units"])
        for unit_class, unit in DEFAULT["display_units"].items():
            if self.DISPLAY_UNITS.get(unit_class, None) is None:
                self.DISPLAY_UNITS[unit_class] = unit
        
        file_paths: dict = config_data.get("file_paths", DEFAULT["file_paths"])
        self.GAME_STATE_FILE_PATH: str = construct_path(file_paths.get("game_state", DEFAULT["file_paths"]["game_state"]))
        self.GLOBAL_STATE_FILE_PATH: str = construct_path(file_paths.get("global_state", DEFAULT["file_paths"]["global_state"]))

        try:
            validator.validate_int(self.DECIMAL_DIGITS, "decimal_digits", 0, 10)
            validator.validate_int(self.DEFAULT_SHIP_CONSOLE_CHAR_DELAY, "default_ship_console_char_delay", 0)
            validator.validate_int(self.DEFAULT_SHIP_CONSOLE_LINE_DELAY, "default_ship_console_line_delay", 0)
            validator.validate_style_tag(self.DEFAULT_SHIP_CONSOLE_STYLE_TAG)
            for unit_class in EXISTING_CLASSES:
                validator.validate_physical_unit_and_class(self.DISPLAY_UNITS[unit_class], unit_class)
            for unit_class in self.DISPLAY_UNITS_CONVENIENCE_THRESHOLD:
                validator.validate_physical_unit_class(unit_class=unit_class)
        except (ValueError, TypeError, KeyError) as e:
            raise RuntimeError(f"An error occured while initializing the config: {e}\nCheck your config at {CONFIG_FILE_PATH}")

    @staticmethod
    def get_instance() -> 'Config':
        if Config._instance is None:
            Config._instance = Config()
        return Config._instance
    
    def is_unit_class_displayed_conveniently(self, unit_class: str) -> bool:
        if unit_class in self.DISPLAY_UNITS_CONVENIENCE_THRESHOLD:
            return True
        return False
    
    def get_display_unit_convenience_treshold(self, unit_class: str) -> float:
        if unit_class not in self.DISPLAY_UNITS_CONVENIENCE_THRESHOLD:
            return 1
        return self.DISPLAY_UNITS_CONVENIENCE_THRESHOLD[unit_class]