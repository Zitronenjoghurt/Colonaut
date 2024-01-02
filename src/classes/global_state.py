from .config import Config
from .save_state import SaveState

CONFIG = Config.get_instance()

class GlobalState(SaveState):
    _instance = None
    SAVE_FILE_PATH = CONFIG.GLOBAL_STATE_FILE_PATH + "global_state." + CONFIG.SAVE_FILE_MODE
    DEFAULT_SAVE_FILE_PATH = CONFIG.DEFAULT_GLOBAL_STATE_FILE_PATH

    def __init__(self, run_count: int, finished_tutorial: bool) -> None:
        if self._instance is not None:
            raise RuntimeError("Tried to initialize two instances of GlobalState.")
        self.run_count = run_count
        self.finished_tutorial = finished_tutorial
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
            "finished_tutorial": data.get("finished_tutorial", None)
        }

        for key, value in retrieved_data.items():
            if value is None:
                raise RuntimeError(f"An error occured while loading the global state save file: missing {key} data.")
        
        return GlobalState(
            run_count=retrieved_data['run_count'],
            finished_tutorial=retrieved_data['finished_tutorial']
        )
    
    def save(self) -> None:
        data = {
            "run_count": self.run_count,
            "finished_tutorial": self.finished_tutorial
        }

        GlobalState.save_data(data=data)