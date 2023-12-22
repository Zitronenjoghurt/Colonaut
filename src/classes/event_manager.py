from .event import Event
from typing import Callable

class EventManager():
    _instance = None

    def __init__(self) -> None:
        self.listeners: dict[str, list[Callable]] = {}

    @staticmethod
    def get_instance() -> 'EventManager':
        if EventManager._instance is None:
            EventManager._instance = EventManager()
        return EventManager._instance
    
    def subscribe(self, event_type: str, listener: Callable) -> None:
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(listener)

    def publish(self, event: Event) -> list:
        if event.type not in self.listeners:
            return []
        
        responses = []
        for listener in self.listeners[event.type]:
            try:
                response = listener(**event.data)
            except Exception as e:
                raise RuntimeError(f"An error occured while publishing event {event}.") from e
            
            if response is not None:
                responses.append(response)
        return responses