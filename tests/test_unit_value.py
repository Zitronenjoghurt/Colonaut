from pytest import approx
from src.planet_generation.unit_value import UnitValue

VALUES = [
    {"mm": 1.496e14, "cm": 1.496e13, "m": 1.496e11, "km": 1.496e8, "AU": 1},
    {"mm^3": 1e18, "cm^3": 1e15, "m^3": 1e9, "km^3": 1},
    {"grm": 5.972e27, "kg": 5.972e24, "t": 5.972e21, "Earth": 1, "Sun": 1/333000},
    {"g/cm^3": 1, "kg/m^3": 1000},
    {"°K": 273.15, "°C": 0, "°F": 32},
    {"°K": 233.15, "°C": -40, "°F": -40},
    {"s": 63115200, "min": 1051920, "h": 17532, "d": 730.5, "y": 2},
    {"km/h": 3600, "m/s": 1000, "km/s": 1},
    {"m/s^2": 9.81, "g": 1}
]

def test_str():
    a = UnitValue(1e7, "km")
    b = UnitValue(1e6, "km")
    c = UnitValue(1e5, "g/cm^3")
    d = UnitValue(1e-1, "m^3")
    e = UnitValue(1e-2, "°C")
    f = UnitValue(1e-3, "kg")

    assert str(a) == "0.07AU"
    assert str(b) == "1000000km"
    assert str(c) == "100000g/cm^3"
    assert str(d) == "0.1m^3"
    assert str(e) == "0.01°C"
    assert str(f) == "1grm"

def test_conversion():
    for unit_values in VALUES:
        units = list(unit_values.keys())
        for unit, value in unit_values.items():
            test_units = [test_unit for test_unit in units if test_unit != unit]
            unit_value = UnitValue(value=value, unit=unit)
            for test_unit in test_units:
                test_value = unit_value.convert(test_unit).get_value()
                assert test_value == approx(unit_values[test_unit], rel=2e-4)

def test_convert_conveniently():
    a = UnitValue(59, "s")
    b = UnitValue(100, "s")
    c = UnitValue(4000, "s")
    d = UnitValue(100000, "s")
    e = UnitValue(5e9, "s")

    assert str(a) == "59s"
    assert str(b) == "1.67min"
    assert str(c) == "1.11h"
    assert str(d) == "1.16d"
    assert str(e) == "158.44y"

def test_to_cubed():
    mm = UnitValue(value=10, unit="mm")
    cm = UnitValue(value=10, unit="cm")
    m = UnitValue(value=10, unit="m")
    km = UnitValue(value=10, unit="km")

    mm_cubed = mm.to_cubed()
    cm_cubed = cm.to_cubed()
    m_cubed = m.to_cubed()
    km_cubed = km.to_cubed()

    assert mm_cubed.get_value() == 1000
    assert cm_cubed.get_value() == 1000
    assert m_cubed.get_value() == 1000
    assert km_cubed.get_value() == 1000

    assert mm_cubed.get_unit() == "mm^3"
    assert cm_cubed.get_unit() == "cm^3"
    assert m_cubed.get_unit() == "m^3"
    assert km_cubed.get_unit() == "km^3"