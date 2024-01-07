class Locales:
    ORB_PERIOD = "orb_period"
    ROT_PERIOD = "rot_period"

    @classmethod
    def get_existing_keys(cls) -> list[str]:
        return [getattr(cls, attr) for attr in dir(cls) if not callable(getattr(cls, attr)) and not attr.startswith("__")]