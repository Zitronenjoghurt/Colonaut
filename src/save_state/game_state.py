from typing import Optional
import src.utils.validator as validator
from src.constants.config import Config
from src.events.event import Event
from src.planet_generation.planet import Planet
from src.events.response import Response
from src.space_ship.space_ship import SpaceShip
from src.save_state.save_state import SaveState
from src.utils.file_operations import construct_path

CONFIG = Config.get_instance()

class GameState(SaveState):
    _instance = None
    SAVE_FILE_PATH = CONFIG.GAME_STATE_FILE_PATH + "game_state." + CONFIG.SAVE_FILE_MODE
    DEFAULT_SAVE_FILE_PATH = construct_path("src/data/default_game_state.json")

    def __init__(self, ship: SpaceShip, matter: int, planet: Optional[Planet]) -> None:
        if self._instance is not None:
            raise RuntimeError("Tried to initialize two instances of GameState.")
        self.ship = ship
        self.matter = matter
        self.planet = planet

        subscriptions = {
            Event.TYPES.GAME_STATE_RETRIEVE_MATTER: self.retrieve_matter,
            Event.TYPES.GAME_STATE_SUBTRACT_MATTER: self.subtract_matter
        }
        super().__init__(subscriptions=subscriptions)

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

        retrieved_data = {
            "ship": data.get("ship", None),
            "matter": data.get("matter", None)
        }

        for key, value in retrieved_data.items():
            if value is None:
                raise RuntimeError(f"An error occured while loading the game state save file: missing {key} data.")
        
        planet_data = data.get("planet", None)
        planet = None
        try:
            ship = SpaceShip.from_dict(retrieved_data["ship"])
            if planet_data:
                planet = Planet.from_dict(planet_data)
            validator.validate_int(data["matter"], "matter", 0)
        except Exception as e:
            raise RuntimeError(f"An error occured while loading the save file: {e}")
        
        return GameState(
            ship=ship,
            planet=planet,
            matter=retrieved_data["matter"]
        )
    
    def save(self) -> None:
        ship_data = self.ship.to_dict().get_data()

        if self.planet:
            planet_data = self.planet.to_dict()
        else:
            planet_data = None

        data = {
            "ship": ship_data,
            "planet": planet_data,
            "matter": self.matter
        }

        GameState.save_data(data=data)

    def retrieve_matter(self) -> Response:
        return Response.create(self.matter, Response.TYPES.AMOUNT_MATTER)
    
    def subtract_matter(self, amount: int) -> Response:
        if amount > self.matter:
            raise RuntimeError(f"An error occured while trying to subtract {amount} matter: player only has {self.matter} matter")
        self.matter -= amount
        return Response.create()