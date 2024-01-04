from src.constants.event_types import EventTypes

class Event():
    TYPES = EventTypes
    
    def __init__(self, type: str, **kwargs) -> None:
        self.type = type
        self.data = kwargs