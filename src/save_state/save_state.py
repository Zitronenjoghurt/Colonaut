from src.constants.config import Config
from src.events.event_subscriber import BaseEventSubscriber
from src.utils.file_operations import file_to_dict, bin_file_to_dict, dict_to_file, dict_to_bin_file, file_exists, delete_file

CONFIG = Config.get_instance()

LOAD_FUNCTIONS = {
    "json": file_to_dict,
    "pkl": bin_file_to_dict
}

SAVE_FUNCTIONS = {
    "json": dict_to_file,
    "pkl": dict_to_bin_file
}

class SaveState(BaseEventSubscriber):
    SAVE_FILE_PATH = ""
    DEFAULT_SAVE_FILE_PATH = ""

    def __init__(self) -> None:
        self.delete_confirmed = False
        super().__init__()

    @classmethod
    def load_data(cls) -> dict:
        if file_exists(cls.SAVE_FILE_PATH):
            data = LOAD_FUNCTIONS[CONFIG.SAVE_FILE_MODE](cls.SAVE_FILE_PATH)
        else:
            data = file_to_dict(cls.DEFAULT_SAVE_FILE_PATH)
        return data
    
    @classmethod
    def save_data(cls, data: dict) -> None:
        SAVE_FUNCTIONS[CONFIG.SAVE_FILE_MODE](cls.SAVE_FILE_PATH, data)

    @classmethod
    def load(cls) -> 'SaveState':
        return SaveState()
    
    def save(self) -> None:
        return

    def delete(self) -> None:
        if not self.delete_confirmed:
            self.delete_confirmed = True
        else:
            delete_file(self.SAVE_FILE_PATH)