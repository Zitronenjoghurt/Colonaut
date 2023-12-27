import os
from .event_subscriber import BaseEventSubscriber
from .space_ship import SpaceShip
from ..modules.utilities import file_to_dict, dict_to_file, file_exists, delete_file

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_FILE_PATH = os.path.join(CURRENT_DIR, '..', 'game_state.json')
DEFAULT_SAVE_FILE_PATH = os.path.join(CURRENT_DIR, '..', 'data', 'default_game_state.json')

class GameState(BaseEventSubscriber):
    _instance = None

    def __init__(self, ship: SpaceShip) -> None:
        if self._instance is not None:
            raise RuntimeError("Tried to initialize two instances of GameState.")
        self.ship = ship
        self.delete_confirmed = False

    @staticmethod
    def get_instance() -> 'GameState':
        if GameState._instance is None:
            GameState._instance = GameState.load()
        return GameState._instance
    
    @staticmethod
    def reset_instance() -> None:
        GameState._instance = None

    @staticmethod
    def load() -> 'GameState':
        if file_exists(SAVE_FILE_PATH):
            data = file_to_dict(SAVE_FILE_PATH)
        else:
            data = file_to_dict(DEFAULT_SAVE_FILE_PATH)

        ship_data = data.get("ship", None)

        if ship_data is None:
            raise RuntimeError("An error occured while loading the save file: missing ship data.")
        try:
            ship = SpaceShip.from_dict(ship_data)
        except Exception as e:
            raise RuntimeError(f"An error occured while loading the save file: {e}")
        
        return GameState(ship=ship)
    
    def save(self) -> None:
        ship_data = self.ship.to_dict().get_data()

        data = {
            "ship": ship_data
        }

        dict_to_file(SAVE_FILE_PATH, data)

    def delete(self) -> None:
        if not self.delete_confirmed:
            self.delete_confirmed = True
        else:
            delete_file(SAVE_FILE_PATH)