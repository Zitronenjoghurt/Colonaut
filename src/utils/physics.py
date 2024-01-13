import math
from src.planet_generation.unit_value import UnitValue

G = 6.6743e-11
ESI_WEIGHTS = {
    "radius": 0.57,
    "density": 1.07,
    "escape_velocity": 0.7,
    "surface_temperature": 5.58
}

EARTH = {
    "radius": UnitValue(6371, "km").convert("m"),
    "density": UnitValue(5.51, "g/cm^3").convert("kg/m^3"),
    "escape_velocity": UnitValue(11.19, "km/s").convert("m/s"),
    "surface_temperature": UnitValue(15, "°C").convert("°K")
}

def sphere_volume(radius: UnitValue) -> UnitValue:
    radius_cubed = radius.to_cubed()
    sphere_volume_value = radius_cubed.value * math.pi * (4/3)

    return UnitValue(value=sphere_volume_value, unit=radius_cubed.unit)

def sphere_mass(radius: UnitValue, density: UnitValue) -> UnitValue:
    radius = radius.convert("m")
    density = density.convert("kg/m^3")

    volume = sphere_volume(radius=radius)

    mass = volume.value * density.value
    return UnitValue(value=mass, unit="kg")

def orbital_period(distance_to_star: UnitValue, mass_star: UnitValue) -> UnitValue:
    a = distance_to_star.convert("m").get_value()
    M1 = mass_star.convert("kg").get_value()

    if M1 == 0:
        return UnitValue.from_zero("time")

    # Mass of the planet is neglegible => M2 = 0
    T = 2 * math.pi * math.sqrt((a**3)/(G*(M1)))

    orb_period = UnitValue(value=T, unit="s")
    return orb_period

def gravity(planet_radius: UnitValue, planet_mass: UnitValue) -> UnitValue:
    r = planet_radius.convert("m").get_value()
    M = planet_mass.convert("kg").get_value()

    if r == 0:
        return UnitValue.from_zero("acceleration")

    g = (G*M)/(r**2)

    planet_gravity = UnitValue(value=g, unit="m/s^2")
    return planet_gravity

def escape_velocity(planet_radius: UnitValue, planet_mass: UnitValue) -> UnitValue:
    r = planet_radius.convert("m").get_value()
    M = planet_mass.convert("kg").get_value()

    if r == 0:
        return UnitValue.from_zero("speed")
    
    v = math.sqrt((2*G*M)/r)

    v_escape = UnitValue(value=v, unit="m/s")
    return v_escape

# Earth Similarity Index
def esi(radius: UnitValue, density: UnitValue, escape_velocity: UnitValue, surface_temperature: UnitValue) -> float:
    planet_data = {
        "radius": radius.convert("m"),
        "density": density.convert("kg/m^3"),
        "escape_velocity": escape_velocity.convert("m/s"),
        "surface_temperature": surface_temperature.convert("°K")
    }

    ESI = {}
    for property in planet_data:
        x_planet = planet_data[property].get_value()
        x_earth = EARTH[property].get_value()
        n = ESI_WEIGHTS[property]

        ESI[property] = 1 - abs((x_planet-x_earth)/(x_planet+x_earth))**(0.5*n)

    esi_product = 1
    for value in ESI.values():
        esi_product *= value
    
    final_esi = esi_product**(1/4)
    return final_esi