class ShipSystemNotFoundError(Exception):
    def __init__(self, system_name: str, *args: object) -> None:
        message = f"Ship system {system_name} not found."
        super().__init__(message, *args)