import src.space_ship.ship_systems as ShipSystems
from src.space_ship.upgrade_model import UpgradeModelLibrary

MODEL_LIBRARY = UpgradeModelLibrary.get_instance()

class ShipSystemFactory():
    REGISTRY = {
        "accelerometer": ShipSystems.Accelerometer,
        "battery": ShipSystems.BatterySystem,
        "hull": ShipSystems.HullSystem,
        "infrared_spectrometer": ShipSystems.InfraredSpectrometer,
        "laser_altimeter": ShipSystems.LaserAltimeter,
        "neutron_densitometer": ShipSystems.NeutronDensitometer,
        "radio_telemetry": ShipSystems.RadioTelemetry,
        "solar_panel": ShipSystems.SolarPanelSystem
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
            raise ValueError(f"Ship system {system_name} not found")
        
        model_name = kwargs.pop("model", "standard")
        
        try:
            model = MODEL_LIBRARY.get_model(system_name=system_name, model_name=model_name)
            for property in model.get_upgrades():
                property_level = int(kwargs[property])
                kwargs[property] = model.get_level_value(property=property, level=property_level)
            return system_class(upgrade_model=model, **kwargs)
        except (TypeError, ValueError) as e:
            raise ValueError(f"An error occured while creating system {system_name}: {e}")
    
    """
    Possible errors:
    - ValueError
    """
    @staticmethod
    def create_from_dict(system_name: str, data: dict):
        return ShipSystemFactory.create(system_name=system_name, **data)