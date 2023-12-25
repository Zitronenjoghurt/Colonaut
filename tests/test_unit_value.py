from src.classes.unit_value import UnitValue

VALUES = [
    {"mm": 1000000, "cm": 100000, "m": 1000, "km": 1},
    {"g": 1000000, "kg": 1000, "t": 1},
    {"g/cm^3": 1, "kg/m^3": 1000},
    {"K": 273.15, "C": 0, "F": 32},
    {"K": 233.15, "C": -40, "F": -40}
]

def test_conversion():
    for unit_values in VALUES:
        units = list(unit_values.keys())
        for unit, value in unit_values.items():
            test_units = [test_unit for test_unit in units if test_unit != unit]
            unit_value = UnitValue(value=value, unit=unit)
            for test_unit in test_units:
                test_value = unit_value.convert(test_unit).value
                assert round(test_value, 2) == unit_values[test_unit]