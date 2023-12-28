from typing import Optional
from .event import Event
from .response import Response
from .event_subscriber import BaseEventSubscriber
from .ship_system import ShipSystem
from .ship_system_factory import ShipSystemFactory
from ..constants.custom_exceptions import ShipSystemNotFoundError

class SpaceShip(BaseEventSubscriber):
    def __init__(self, systems: Optional[dict[str, ShipSystem]] = None) -> None:
        self.SUBSCRIPTIONS = {
            Event.TYPES.SHIP_RETRIEVE_SYSTEM: self.get_system,
            Event.TYPES.SHIP_DAMAGE_SYSTEM: self.damage_system,
            Event.TYPES.RETRIEVE_SHIP_DATA: self.get_current_status
        }
        super().__init__()
        if systems is None:
            systems = {}
        self.systems: dict[str, ShipSystem] = systems
        self.scanner_results: list[str] = []

    @staticmethod
    def from_dict(data: dict) -> 'SpaceShip':
        systems_data: dict[str, dict] = data.get("systems", None)
        if systems_data is None:
            raise ValueError("Space ship data has no specified systems.")
        
        systems = {}
        for system_name, system_dict in systems_data.items():
            system = ShipSystemFactory.create_from_dict(system_name=system_name, data=system_dict)
            systems[system_name] = system
        return SpaceShip(systems=systems)

    def to_dict(self) -> Response:
        systems = {}
        for system in self.systems.values():
            systems[system.NAME] = system.to_dict().get_data()
        
        result = {
            "systems": systems
        }
        return Response.from_data(result)
    
    def run(self) -> None:
        self.run_systems()
    
    def run_systems(self) -> None:
        self.scanner_results = []
        for system in self.systems.values():
            response = system.work()
            self.handle_system_response(response)
    
    def handle_system_response(self, response: Response) -> None:
        match response.get_type():
            case Response.TYPES.SCANNER_RESULT:
                self.scanner_results.extend(response.get_data())

    """
    Possible errors:
    - ShipSystemNotFoundError
    - ValueError
    """
    def damage_system(self, system_name: str, amount: int) -> Response:
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
    
    def get_current_status(self) -> Response:
        data = []
        for system in self.systems.values():
            data.append(system.get_current_status().get_data())
        return Response.from_data(data, Response.TYPES.SHIP_DATA)