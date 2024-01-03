from .config import Config
from .save_state import SaveState

CONFIG = Config.get_instance()

class GlobalState(SaveState):
    _instance = None
    SAVE_FILE_PATH = CONFIG.GLOBAL_STATE_FILE_PATH + "global_state." + CONFIG.SAVE_FILE_MODE
    DEFAULT_SAVE_FILE_PATH = CONFIG.DEFAULT_GLOBAL_STATE_FILE_PATH

    def __init__(self, run_count: int, finished_intro: bool) -> None:
        if self._instance is not None:
            raise RuntimeError("Tried to initialize two instances of GlobalState.")
        self.run_count = run_count
        self.finished_intro = finished_intro
        super().__init__()

    @staticmethod
    def get_instance() -> 'GlobalState':
        if GlobalState._instance is None:
            GlobalState._instance = GlobalState.load()
        return GlobalState._instance
    
    @staticmethod
    def reset_instance() -> None:
        GlobalState._instance = None

    @staticmethod
    def load() -> 'GlobalState':
        data = GlobalState.load_data()

        retrieved_data = {
            "run_count": data.get("run_count", None),
            "finished_intro": data.get("finished_intro", None)
        }

        for key, value in retrieved_data.items():
            if value is None:
                raise RuntimeError(f"An error occured while loading the global state save file: missing {key} data.")
        
        return GlobalState(
            run_count=retrieved_data['run_count'],
            finished_intro=retrieved_data['finished_intro']
        )
    
    def save(self) -> None:
        data = {
            "run_count": self.run_count,
            "finished_intro": self.finished_intro
        }

        GlobalState.save_data(data=data)