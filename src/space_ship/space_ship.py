from typing import Optional
from src.space_ship.ship_system import ShipSystem
from src.space_ship.ship_system_factory import ShipSystemFactory
from src.constants.custom_exceptions import ShipSystemNotFoundError
from src.events.event import Event
from src.events.response import Response
from src.events.event_subscriber import BaseEventSubscriber

class SpaceShip(BaseEventSubscriber):
    def __init__(self, systems: Optional[dict[str, ShipSystem]] = None) -> None:
        subscriptions = {
            Event.TYPES.SHIP_RETRIEVE_SYSTEM: self.get_system,
            Event.TYPES.SHIP_DAMAGE_SYSTEM: self.damage_system,
            Event.TYPES.RETRIEVE_SHIP_STATUS: self.get_status,
            Event.TYPES.RETRIEVE_SYSTEM_WINDOW_DATA: self.get_system_window_data
        }
        super().__init__(subscriptions=subscriptions)
        if systems is None:
            systems = {}
        self.systems: dict[str, ShipSystem] = systems
        self.scanner_results: list[str] = []
        self.status_log: list[str] = []

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
        return Response.create(result)
    
    def run(self) -> None:
        self.run_systems()
    
    def run_systems(self) -> None:
        self.scanner_results = []
        for system in self.systems.values():
            response = system.work()
            self.handle_system_response(response)
    
    def handle_system_response(self, response: Response) -> None:
        scanner_result = response.get_data(Response.TYPES.SCANNER_RESULT)
        status_log = response.get_data(Response.TYPES.SHIP_STATUS_LOG_ENTRY)
        if scanner_result:
            self.scanner_results.extend(scanner_result)
        if status_log:
            if isinstance(status_log, list):
                self.status_log.extend(status_log)
            else:
                self.status_log.append(status_log)

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
        return Response.create(f"{system_name.capitalize()} took {amount} damage.")

    """
    Possible errors:
    - ShipSystemNotFoundError
    """
    def get_system(self, system_name: str) -> Response:
        system = self.systems.get(system_name, None)

        if not system_name or not isinstance(system, ShipSystem):
            raise ShipSystemNotFoundError(system_name=system_name)
        
        return Response.create(data=system)
    
    def get_status(self) -> Response:
        data = {}
        
        for system_name, system in self.systems.items():
            data[system_name] = system.get_status().get_data()
        response = Response.create(data, Response.TYPES.SHIP_DATA)

        response.add_data(self.status_log, Response.TYPES.SHIP_STATUS_LOG)
        self.status_log = []
        return response
    
    """
    Possible errors:
    - ShipSystemNotFoundError
    """
    def get_system_window_data(self, system_name: str) -> Response:
        system: ShipSystem = self.get_system(system_name=system_name).get_data()
        return system.get_system_window_data()