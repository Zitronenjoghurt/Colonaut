from .event_subscriber import BaseEventSubscriber
from .game_state import GameState
from .global_state import GlobalState

class GameManager(BaseEventSubscriber):
    _instance = None

    def __init__(self) -> None:
        if self._instance is not None:
            raise RuntimeError("Tried to initialize two instances of GameManager.")
        self.game_state = GameState.get_instance()
        self.global_state = GlobalState.get_instance()

    @staticmethod
    def get_instance() -> 'GameManager':
        if GameManager._instance is None:
            GameManager._instance = GameManager()
        return GameManager._instance
    
    @staticmethod
    def reset_instance() -> None:
        GameManager._instance = None
        GameState.reset_instance()
        GlobalState.reset_instance()