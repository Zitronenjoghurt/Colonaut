from src.constants.config import Config
from src.events.event_subscriber import BaseEventSubscriber
from src.utils.file_operations import file_to_dict, cbor_file_to_dict, dict_to_file, dict_to_cbor_file, file_exists, delete_file

CONFIG = Config.get_instance()

LOAD_FUNCTIONS = {
    "json": file_to_dict,
    "cbor": cbor_file_to_dict
}

SAVE_FUNCTIONS = {
    "json": dict_to_file,
    "cbor": dict_to_cbor_file
}

class SaveState(BaseEventSubscriber):
    SAVE_FILE_PATH = ""
    DEFAULT_SAVE_FILE_PATH = ""

    def __init__(self, subscriptions = None) -> None:
        self.delete_confirmed = False
        super().__init__(subscriptions=subscriptions)

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