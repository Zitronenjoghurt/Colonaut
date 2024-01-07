class Locales:
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