from typing import Callable
from .event import Event
from .response import Response
from ..constants.custom_exceptions import EventTypeNotSubscribedError

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
    
    @staticmethod
    def reset_instance() -> None:
        EventBus._instance = None
    
    """
    Possible errors:
    - RuntimeError
    """
    def subscribe(self, event_type: str, listener: Callable) -> None:
        if self.listeners.get(event_type, None) is not None:
            raise RuntimeError(f"Subscription on event type {event_type} already exists.")
        self.listeners[event_type] = listener

    """
    Possible errors:
    - RuntimeError
    """
    def unsubscribe(self, event_type: str, listener: Callable) -> None:
        if self.listeners.get(event_type, None) is None:
            raise RuntimeError(f"Subscription on event type {event_type} does not exist.")
        self.listeners.pop(event_type)

    """
    Possible errors:
    - EventTypeNotSubscribedError
    - RuntimeError
    """
    def publish(self, event: Event) -> Response:
        if event.type not in self.listeners:
            raise EventTypeNotSubscribedError(event_type=event.type)
        
        listener = self.listeners[event.type]
        try:
            response = listener(**event.data)
        except Exception as e:
            raise RuntimeError(f"An error occured while publishing event {event}.") from e
        
        return response