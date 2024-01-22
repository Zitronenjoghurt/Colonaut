from src.molecule_database.aggregate_states import AggregateState
from src.planet_generation.unit_value import UnitValue

class Molecule():
    def __init__(self, name: str, symbol: str, melting_point: UnitValue, boiling_point: UnitValue) -> None:
        melting_point.validate_of_class("temperature")
        boiling_point.validate_of_class("temperature")

        self.name = name
        self.symbol = symbol
        self.melting_point = melting_point.convert("°K")
        self.boiling_point = boiling_point.convert("°K")

    @staticmethod
    def from_dict(data: dict) -> 'Molecule':
        retrieved_data = {
            "name": data.get("name", None),
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
                raise ValueError(f"Failed to initialize molecule from dictionary: missing key {key}")
            
        return Molecule(**retrieved_data)
    
    def get_name(self) -> str:
        return self.name
    
    def get_symbol(self) -> str:
        return self.symbol
    
    def get_melting_point(self) -> UnitValue:
        return self.melting_point
    
    def get_boiling_point(self) -> UnitValue:
        return self.boiling_point
    
    def get_state_at(self, temperature: UnitValue) -> AggregateState:
        temperature.validate_of_class("temperature")
        current_temp = temperature.convert("°K").get_value()

        if current_temp < self.melting_point.get_value():
            return AggregateState.SOLID
        
        if current_temp > self.boiling_point.get_value():
            return AggregateState.GASEOUS
        
        return AggregateState.LIQUID