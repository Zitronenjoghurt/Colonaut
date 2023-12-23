from .event_subscriber import BaseEventSubscriber
from .response import Response

class ShipSystem(BaseEventSubscriber):
    NAME = "default"

    def __init__(self, max_hitpoints: int) -> None:
        self.max_hitpoints = max_hitpoints
        self.hitpoints = max_hitpoints

    def get_name(self) -> str:
        return self.NAME
    
    """
    Possible errors:
    - ValueError
    """
    def damage(self, amount: int) -> Response:
        if not isinstance(amount, int):
            raise ValueError("Amount must be of type int.")
        if amount < 0:
            raise ValueError("Amount must be greater or equal 0.")
        self.hitpoints -= amount

        if self.hitpoints < 0:
            self.hitpoints = 0

        return Response.create()

class HullSystem(ShipSystem):
    NAME = "hull"

    def __init__(self, max_hitpoints: int) -> None:


        super().__init__(max_hitpoints=max_hitpoints)

class BatterySystem(ShipSystem):
    NAME = "battery"

    def __init__(self, max_hitpoints: int, max_capacity: int) -> None:
        self.max_capacity = max_capacity
        self.capacity = max_capacity

        super().__init__(max_hitpoints=max_hitpoints)