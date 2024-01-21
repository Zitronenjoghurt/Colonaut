from src.planet_generation.unit_value import UnitValue

class Element():
    def __init__(self, name: str, atomic_number: int, symbol: str, melting_point: UnitValue, boiling_point: UnitValue) -> None:
        melting_point.validate_of_class("temperature")
        boiling_point.validate_of_class("temperature")

        self.name = name
        self.atomic_number = atomic_number
        self.symbol = symbol
        self.melting_point = melting_point
        self.boiling_point = boiling_point

    @staticmethod
    def from_dict(data: dict) -> 'Element':
        retrieved_data = {
            "name": data.get("name", None),
            "atomic_number": data.get("atomic_number", None),
            "symbol": data.get("symbol", None),
            "melting_point": None,
            "boiling_point": None
        }

        melting_point = data.get("melting_point", None)
        if isinstance(melting_point, (str, dict)):
            retrieved_data["melting_point"] = UnitValue.from_any(melting_point)
        boiling_point = data.get("boiling_point", None)
        if isinstance(boiling_point, (str, dict)):
            retrieved_data["boiling_point"] = UnitValue.from_any(boiling_point)

        for key, value in retrieved_data.items():
            if value is None:
                raise ValueError(f"Failed to initialize element from dictionary: missing key {key}")
            
        return Element(**retrieved_data)