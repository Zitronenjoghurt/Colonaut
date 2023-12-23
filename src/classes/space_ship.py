from .event import Event
from .event_subscriber import BaseEventSubscriber

class SpaceShip(BaseEventSubscriber):
    def __init__(self) -> None:
        self.SUBSCRIPTIONS = {
            Event.TYPES.SHIP_SYSTEM_DAMAGE: self.damage_system
        }
        super().__init__()
        self.hull = 100

    def damage_system(self, system: str, amount: int) -> None:
        pass