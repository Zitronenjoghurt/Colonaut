from typing import Optional
from .event import Event
from .event_subscriber import BaseEventSubscriber
from .game_state import GameState
from .global_state import GlobalState
from .planet import Planet, PlanetGenerator
from .response import Response
from ..ui.ui_system import UISystem

class GameManager(BaseEventSubscriber):
    _instance = None

    def __init__(self) -> None:
        if self._instance is not None:
            raise RuntimeError("Tried to initialize two instances of GameManager.")
        self.game_state = GameState.get_instance()
        self.global_state = GlobalState.get_instance()
        self.ui_system = UISystem()

        self.current_planet: Optional[Planet] = None
        
        subscriptions = {
            Event.TYPES.GAME_FLOW_FINISH_INTRO: self.finish_intro,
            Event.TYPES.GAME_FLOW_JUMP: self.jump,
            Event.TYPES.RETRIEVE_PLANET_DATA: self.retrieve_planet_data
        }
        super().__init__(subscriptions=subscriptions)

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

    def save_state(self) -> None:
        self.game_state.save()
        self.global_state.save()

    def start(self) -> None:
        if not self.global_state.finished_intro:
            mode = "intro"
        elif not self.global_state.finished_tutorial:
            mode = "tutorial"
        else:
            mode = "game"
        self.ui_system.start(mode=mode)

    """
    Event driven functions
    """
    def jump(self) -> Response:
        self.current_planet = PlanetGenerator.generate()
        self.game_state.ship.run()
        return Response.create()
    
    def retrieve_planet_data(self) -> Response:
        if self.current_planet:
            planet_data = self.current_planet.get_data()
        else:
            planet_data = []
        return Response.create(planet_data, Response.TYPES.PLANET_DATA)
    
    def finish_intro(self) -> Response:
        self.global_state.finished_intro = True
        self.ui_system.start_tutorial()
        return Response.create()