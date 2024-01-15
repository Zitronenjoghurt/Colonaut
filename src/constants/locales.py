# These constants will mainly be used to validate locale files.
# But they also make locale strings easily accessible when you 
# need specific ones, preventing error caused by typos.
class Locales:
    # Common
    FAILURE = "failure"
    SUCCESS = "success"

    # Descriptions
    ACCELEROMETER_DESCRIPTION = "accelerometer_description"
    BATTERY_DESCRIPTION = "battery_description"
    HULL_DESCRIPTION = "hull_description"
    INFRARED_SPECTROMETER_DESCRIPTION = "infrared_spectrometer_description"
    LASER_ALTIMETER_DESCRIPTION = "laser_altimeter_description"
    NEUTRON_DENSITOMETER_DESCRIPTION = "neutron_densitometer_description"
    PLANET_ICE_DESCRIPTION = "planet_ice_description"
    RADIO_TELEMETRY_DESCRIPTION = "radio_telemetry_description"
    SOLAR_PANEL_DESCRIPTION = "solar_panel_description"

    # Messages
    BATTERY_CHARGED_BY = "battery_charged_by"
    BATTERY_DISTRIBUTED_ENERGY = "battery_distributed_energy"
    BATTERY_FULLY_CHARGED = "battery_fully_charged"
    BATTERY_WARNING_NET_NEGATIVE_ENERGY = "battery_warning_net_negative_energy"
    SOLAR_PANEL_COLLECTED_ENERGY = "solar_panel_collected_energy"
    SOLAR_PANEL_NO_BATTERY = "solar_panel_no_battery"

    # Names
    ACCELEROMETER = "accelerometer"
    BATTERY = "battery"
    HULL = "hull"
    INFRARED_SPECTROMETER = "infrared_spectrometer"
    LASER_ALTIMETER = "laser_altimeter"
    NEUTRON_DENSITOMETER = "neutron_densitometer"
    PLANET_ICE = "planet_ice"
    RADIO_TELEMETRY = "radio_telemetry"
    SOLAR_PANEL = "solar_panel"

    # Science
    AXIAL_TILT = "axial_tilt"
    DENSITY = "density"
    DISTANCE_TO_STAR = "distance_to_star"
    ESCAPE_VELOCITY = "escape_velocity"
    ESI = "esi"
    GRAVITY = "gravity"
    MASS = "mass"
    ORB_PERIOD = "orb_period"
    RADIUS = "radius"
    ROT_PERIOD = "rot_period"
    STAR_MASS = "star_mass"
    TEMPERATURE = "temperature"
    VOLUME = "volume"

    # Stats
    CAPACITY = "capacity"
    CHARGE_CAPACITY = "charge_capacity"
    HEALTH = "health"
    MAX_CAPACITY = "max_capacity"
    MAX_HP = "max_hp"
    POWER = "power"
    POWER_USAGE = "power_usage"
    REVEAL_CHANCE = "reveal_chance"
    SUCCESS_RATE = "success_rate"

    # TOPOGRAPHY
    CREVASSE_FIELDS = "crevasse_fields"
    CRYOVOLCANOES = "cryovolcanoes"
    FROST_MOUNTAINS = "frost_mountains"
    FROZEN_LAKES = "frozen_lakes"
    FROZEN_SEAS = "frozen_seas"
    GLACIAL_VALLES = "glacial_valleys"
    ICEBERGS = "icebergs"
    ICE_CAVES = "ice_caves"
    ICE_DUNES = "ice_dunes"
    ICE_CLIFFS = "ice_cliffs"
    ICE_PLAINS = "ice_plains"
    SNOW_FIELDS = "snow_fields"
    SUBSURFACE_OCEANS = "subsurface_oceans"

    # UI
    ADDITIONAL_INFORMATION = "additional_information"
    INSPIRED_BY_SEEDSHIP = "inspired_by_seedship"
    OPTIONS = "options"
    PLANET_REPORT = "planet_report"
    QUIT = "quit"
    REALLY_QUIT = "really_quit"
    START_GAME = "start_game"
    STATS = "stats"

    @classmethod
    def get_existing_keys(cls) -> list[str]:
        return [getattr(cls, attr) for attr in dir(cls) if not callable(getattr(cls, attr)) and not attr.startswith("__")]