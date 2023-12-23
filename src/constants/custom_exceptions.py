class EventTypeNotSubscribedError(Exception):
    def __init__(self, event_type: str) -> None:
        message = f"Event type {event_type} has no listener yet."
        super().__init__(message)

class ShipSystemNotFoundError(Exception):
    def __init__(self, system_name: str) -> None:
        message = f"Ship system {system_name} not found."
        super().__init__(message)