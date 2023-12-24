from .ship_systems import BatterySystem, HullSystem, SolarPanelSystem

class ShipSystemFactory():
    REGISTRY = {
        "hull": HullSystem,
        "battery": BatterySystem,
        "solar panel": SolarPanelSystem
    }

    """
    Possible errors:
    - ValueError
    """
    @staticmethod
    def create(system_name: str, **kwargs):
        system_name = system_name.lower()
        system_class = ShipSystemFactory.REGISTRY.get(system_name, None)

        if system_class is None:
            raise ValueError(f"Ship system {system_name} not found.")
        try:
            return system_class(**kwargs)
        except TypeError as e:
            raise ValueError(f"An error occured while creating system {system_name}: {e}")
    
    """
    Possible errors:
    - ValueError
    """
    @staticmethod
    def create_from_dict(system_name: str, data: dict):
        return ShipSystemFactory.create(system_name=system_name, **data)