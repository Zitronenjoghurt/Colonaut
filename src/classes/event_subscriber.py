from typing import Callable, Optional
from .event_bus import EventBus
from .response import Response

# A base class, inherited if event functionalities are required
class BaseEventSubscriber():

    def __init__(self, subscriptions: Optional[dict[str, Callable]] = None) -> None:
        if subscriptions is None:
            subscriptions = {}
        self.subscriptions = subscriptions
        self.event_bus = EventBus.get_instance()
        self.init_subscriptions()

    def init_subscriptions(self) -> None:
        for event_type, listener in self.subscriptions.items():
            self.event_bus.subscribe(event_type=event_type, listener=listener)

    def unsubcribe_events(self) -> None:
        for event_type, listener in self.subscriptions.items():
            self.event_bus.unsubscribe(event_type=event_type, listener=listener)

    def publish_event(self, event) -> Response:
        return self.event_bus.publish(event=event)