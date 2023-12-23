from typing import Callable
from .event import Event
from .response import Response

class EventBus():
    _instance = None

    def __init__(self) -> None:
        if EventBus._instance is not None:
            raise RuntimeError("Tried to initialize multiple instances of EventBus.")
        
        self.listeners: dict[str, Callable] = {}

    @staticmethod
    def get_instance() -> 'EventBus':
        if EventBus._instance is None:
            EventBus._instance = EventBus()
        return EventBus._instance
    
    def subscribe(self, event_type: str, listener: Callable) -> None:
        if self.listeners.get(event_type, None) is not None:
            raise RuntimeError(f"Subscription on event type {event_type} already exists.")
        self.listeners[event_type] = listener

    def publish(self, event: Event) -> Response:
        if event.type not in self.listeners:
            raise ValueError(f"Event type {event.type} has no listener.")
        
        listener = self.listeners[event.type]
        try:
            response = listener(**event.data)
        except Exception as e:
            raise RuntimeError(f"An error occured while publishing event {event}.") from e
        
        return response