import math
from src.planet_generation.unit_value import UnitValue

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