from .config import Config
from .save_state import SaveState
from .space_ship import SpaceShip

CONFIG = Config.get_instance()

class GameState(SaveState):
    _instance = None
    SAVE_FILE_PATH = CONFIG.GAME_STATE_FILE_PATH + "game_state." + CONFIG.SAVE_FILE_MODE
    DEFAULT_SAVE_FILE_PATH = CONFIG.DEFAULT_GAME_STATE_FILE_PATH

    def __init__(self, ship: SpaceShip) -> None:
        if self._instance is not None:
            raise RuntimeError("Tried to initialize two instances of GameState.")
        self.ship = ship
        super().__init__()

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
        data = GameState.load_data()

        ship_data = data.get("ship", None)

        if ship_data is None:
            raise RuntimeError("An error occured while loading the game state save file: missing ship data.")
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

        GameState.save_data(data=data)