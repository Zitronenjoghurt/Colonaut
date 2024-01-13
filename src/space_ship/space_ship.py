from collections import OrderedDict
from typing import Optional
from src.space_ship.ship_system import ShipSystem
from src.space_ship.ship_system_factory import ShipSystemFactory
from src.constants.custom_exceptions import ShipSystemNotFoundError
from src.events.event import Event
from src.events.response import Response
from src.events.event_subscriber import BaseEventSubscriber

class SpaceShip(BaseEventSubscriber):
    def __init__(self, systems: Optional[dict[str, ShipSystem]] = None, scanner_results: Optional[list[str]] = None) -> None:
        subscriptions = {
            Event.TYPES.SHIP_RETRIEVE_SYSTEM: self.get_system,
            Event.TYPES.SHIP_DAMAGE_SYSTEM: self.damage_system,
            Event.TYPES.SHIP_UPGRADE_SYSTEM: self.upgrade_system,
            Event.TYPES.RETRIEVE_SHIP_STATUS: self.get_status,
            Event.TYPES.RETRIEVE_SYSTEM_UPGRADES: self.get_system_upgrades,
            Event.TYPES.RETRIEVE_SYSTEM_WINDOW_DATA: self.get_system_window_data
        }
        super().__init__(subscriptions=subscriptions)
        if systems is None:
            systems = {}
        if scanner_results is None:
            scanner_results = []
        sorted_systems: list[tuple[str, ShipSystem]] = sorted(systems.items(), key=lambda system: system[1].WORK_ORDER_PRIORITY, reverse=True)
        self.systems: dict[str, ShipSystem] = dict(sorted_systems)

        # Ship system dashboard order priority
        sorted_systems : list[tuple[str, ShipSystem]] = sorted(systems.items(), key=lambda system: system[1].DASHBOARD_ORDER_PRIORITY, reverse=True)
        self._systems_dashboard_order = dict(sorted_systems)

        # The unveiled planet data types
        self.scanner_results: list[str] = scanner_results

        # The status log contain all messages that are printed to the console after the jump
        self.status_log: list[str] = []

    @staticmethod
    def from_dict(data: dict) -> 'SpaceShip':
        systems_data: dict[str, dict] = data.get("systems", None)
        if systems_data is None:
            raise ValueError("Space ship data has no specified systems.")
        
        scanner_results = data.get("scanner_results", None)
        
        systems = {}
        for system_name, system_dict in systems_data.items():
            system = ShipSystemFactory.create_from_dict(system_name=system_name, data=system_dict)
            systems[system_name] = system
        return SpaceShip(systems=systems, scanner_results=scanner_results)

    def to_dict(self) -> Response:
        systems = {}
        for system in self.systems.values():
            systems[system.NAME] = system.to_dict().get_data()
        
        result = {
            "systems": systems,
            "scanner_results": self.scanner_results
        }
        return Response.create(result)
    
    def run(self) -> None:
        self.run_systems()
        self.retrieve_drawn_energy_log()
        self.check_for_additional_data()
    
    def run_systems(self) -> None:
        self.scanner_results = []
        for system in self.systems.values():
            response = system.work()
            self.handle_system_response(response)

    def retrieve_drawn_energy_log(self) -> None:
        battery_drawn_energy_event = Event(Event.TYPES.BATTERY_RETRIEVE_DRAWN_ENERGY_LOG)
        response = self.publish_event(battery_drawn_energy_event)
        logs = response.get_data(Response.TYPES.BATTERY_DRAWN_ENERGY_LOG)
        
        if logs and isinstance(logs, list):
            self.status_log.extend(logs)

    # Depending on the data collected by the scanners, additional data will become available
    def check_for_additional_data(self) -> None:
        additional_data = {
            "esi": ["temperature", "density", "radius", "escape_velocity"]
        }

        available_data = set(self.scanner_results)
        for property, requirements in additional_data.items():
            if set(requirements).issubset(available_data):
                self.scanner_results.append(property)
    
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
        
        for system_name, system in self._systems_dashboard_order.items():
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
    
    """
    Possible errors:
    - ShipSystemNotFoundError
    """
    def get_system_upgrades(self, system_name: str) -> Response:
        system: ShipSystem = self.get_system(system_name=system_name).get_data()
        return system.get_upgrades()
    
    def upgrade_system(self, system_name: str, property: str) -> Response:
        system: ShipSystem = self.get_system(system_name=system_name).get_data()
        try:
            response = system.upgrade_property(property=property)
            cost = response.get_data(Response.TYPES.UPGRADE_COST)
            subtract_matter_event = Event(Event.TYPES.GAME_STATE_SUBTRACT_MATTER, amount=cost)
            self.publish_event(subtract_matter_event)
        except Exception as e:
            raise RuntimeError(f"An error occured while upgrading property {property} of system {system_name}: {e}")
        return Response.create()