from typing import Callable
from .event_bus import EventBus

# A base class, inherited if event functionalities are required
class EventSubscriber():
    SUBSCRIPTIONS: dict[str, Callable] = {}

    def __init__(self) -> None:
        self.event_manager = EventBus.get_instance()
        self.init_subscriptions()

    def init_subscriptions(self):
        for event_type, listener in self.SUBSCRIPTIONS.items():
            self.event_manager.subscribe(event_type=event_type, listener=listener)

    def publish_event(self, event):
        self.event_manager.publish(event=event)