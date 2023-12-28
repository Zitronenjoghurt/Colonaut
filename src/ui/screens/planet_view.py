import urwid
from src.ui.components import DataList
from src.classes.event import Event
from src.classes.response import Response
from src.ui.screen import Screen

class PlanetViewScreen(Screen):
    def __init__(self, screen_manager):
        data = []
        self.data_list = DataList(data=data)
        super().__init__(screen_manager=screen_manager)
        
    def create_layout(self):
        planet_filler = urwid.Filler(self.data_list, valign='middle')
        return planet_filler
    
    def update_planet_data(self, data: list[tuple]) -> None:
        self.data_list.update_data(new_data=data)

    def keypress(self, size, key):
        if key in ('j', 'J'):
            jump_event = Event(Event.TYPES.GAME_FLOW_JUMP)
            planet_data_response: Response = self.manager.publish_event(jump_event)
            if planet_data_response.get_type() == Response.TYPES.PLANET_DATA:
                planet_data = planet_data_response.get_data()
                self.update_planet_data(planet_data)
        super().keypress(size=size, key=key)