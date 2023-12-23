from .event import Event
from .response import Response
from .event_subscriber import BaseEventSubscriber
from .ship_system import ShipSystem
from ..constants.custom_exceptions import ShipSystemNotFoundError

class SpaceShip(BaseEventSubscriber):
    def __init__(self) -> None:
        self.SUBSCRIPTIONS = {
            Event.TYPES.SHIP_RETRIEVE_SYSTEM: self.get_system,
            Event.TYPES.SHIP_SYSTEM_DAMAGE: self.on_system_damage
        }
        super().__init__()
        self.systems: dict[str, ShipSystem] = {}

    """
    Possible errors:
    - ShipSystemNotFoundError
    - ValueError
    """
    def on_system_damage(self, system_name: str, amount: int) -> Response:
        system_name = system_name.lower()
        system_response = self.get_system(system_name=system_name)
        system: ShipSystem = system_response.get_data()

        system.damage(amount=amount)
        return Response.create(message=f"{system_name.capitalize()} took {amount} damage.")

    """
    Possible errors:
    - ShipSystemNotFoundError
    """
    def get_system(self, system_name: str) -> Response:
        system = self.systems.get(system_name, None)

        if not system_name or not isinstance(system, ShipSystem):
            raise ShipSystemNotFoundError(system_name=system_name)
        
        return Response.create(data=system)