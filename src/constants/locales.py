# These constants will mainly be used to validate locale files.
# But they also make locale strings easily accessible when you 
# need specific ones, preventing error caused by typos.
class Locales:
    # Descriptions
    ACCELEROMETER_DESCRIPTION = "accelerometer_description"
    BATTERY_DESCRIPTION = "battery_description"
    HULL_DESCRIPTION = "hull_description"
    INFRARED_SPECTROMETER_DESCRIPTION = "infrared_spectrometer_description"
    LASER_ALTIMETER_DESCRIPTION = "laser_altimeter_description"
    NEUTRON_DENSITOMETER_DESCRIPTION = "neutron_densitometer_description"
    RADIO_TELEMETRY_DESCRIPTION = "radio_telemetry_description"
    SOLAR_PANEL_DESCRIPTION = "solar_panel_description"

    # Names
    ACCELEROMETER = "accelerometer"
    BATTERY = "battery"
    HULL = "hull"
    INFRARED_SPECTROMETER = "infrared_spectrometer"
    LASER_ALTIMETER = "laser_altimeter"
    NEUTRON_DENSITOMETER = "neutron_densitometer"
    RADIO_TELEMETRY = "radio_telemetry"
    SOLAR_PANEL = "solar_panel"

    # Science
    DENSITY = "density"
    MASS = "mass"
    ORB_PERIOD = "orb_period"
    RADIUS = "radius"
    ROT_PERIOD = "rot_period"
    TEMPERATURE = "temperature"
    VOLUME = "volume"

    # Stats
    CHARGE_CAPACITY = "charge_capacity"
    MAX_CAPACITY = "max_capacity"
    MAX_HP = "max_hp"
    REVEAL_CHANCE = "reveal_chance"

    @classmethod
    def get_existing_keys(cls) -> list[str]:
        return [getattr(cls, attr) for attr in dir(cls) if not callable(getattr(cls, attr)) and not attr.startswith("__")]