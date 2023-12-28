import src.ui.components as Components
from src.classes.event import Event
from src.classes.response import Response
from src.ui.screen import Screen

class PlanetViewScreen(Screen):
    def __init__(self, ui_system):
        super().__init__(ui_system=ui_system)
        self.data_list = Components.DataList(self, [])
        self.data_list.pack(side='left', pady=(20, 0), padx=(5, 0))

    def jump(self) -> None:
        jump_event = Event(Event.TYPES.GAME_FLOW_JUMP)
        response: Response = self.ui_system.publish_event(jump_event)
        if response.of_type(Response.TYPES.PLANET_DATA):
            self.data_list.update_data(response.get_data())

    def on_keypress(self, event) -> None:
        super().on_keypress(event)
        if event.keysym in ['j', 'J']:
            self.jump()