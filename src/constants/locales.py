class Locales:
    DENSITY = "density"
    MASS = "mass"
    ORB_PERIOD = "orb_period"
    RADIUS = "radius"
    ROT_PERIOD = "rot_period"
    TEMPERATURE = "temperature"
    VOLUME = "volume"

    @classmethod
    def get_existing_keys(cls) -> list[str]:
        return [getattr(cls, attr) for attr in dir(cls) if not callable(getattr(cls, attr)) and not attr.startswith("__")]