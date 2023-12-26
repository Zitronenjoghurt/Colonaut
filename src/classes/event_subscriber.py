from typing import Callable
from .event_bus import EventBus
from .response import Response

# A base class, inherited if event functionalities are required
class BaseEventSubscriber():
    SUBSCRIPTIONS: dict[str, Callable] = {}

    def __init__(self) -> None:
        self.event_bus = EventBus.get_instance()
        self.init_subscriptions()

    def init_subscriptions(self) -> None:
        for event_type, listener in self.SUBSCRIPTIONS.items():
            self.event_bus.subscribe(event_type=event_type, listener=listener)

    def unsubcribe_events(self) -> None:
        for event_type, listener in self.SUBSCRIPTIONS.items():
            self.event_bus.unsubscribe(event_type=event_type, listener=listener)

    def publish_event(self, event) -> Response:
        return self.event_bus.publish(event=event)