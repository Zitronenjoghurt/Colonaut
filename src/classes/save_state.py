from .event_subscriber import BaseEventSubscriber
from ..modules.utilities import file_to_dict, dict_to_file, file_exists, delete_file, construct_path

class SaveState(BaseEventSubscriber):
    SAVE_FILE_PATH = ""
    DEFAULT_SAVE_FILE_PATH = ""

    def __init__(self) -> None:
        self.delete_confirmed = False
        super().__init__()

    @classmethod
    def load_data(cls) -> dict:
        if file_exists(cls.SAVE_FILE_PATH):
            data = file_to_dict(cls.SAVE_FILE_PATH)
        else:
            data = file_to_dict(cls.DEFAULT_SAVE_FILE_PATH)
        return data
    
    @classmethod
    def save_data(cls, data: dict) -> None:
        dict_to_file(cls.SAVE_FILE_PATH, data)

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