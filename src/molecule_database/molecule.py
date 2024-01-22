from numbers import Number
from src.molecule_database.aggregate_states import AggregateState
from src.planet_generation.probability import Probability
from src.planet_generation.unit_value import UnitValue
from src.utils.validator import validate_of_type

class Molecule():
    def __init__(
            self, 
            name: str, 
            symbol: str, 
            melting_point: UnitValue, 
            boiling_point: UnitValue, 
            exist_weight: int,
            concentration_weight: Probability
        ) -> None:
        validate_of_type(name, str, "name")
        validate_of_type(symbol, str, "symbol")
        melting_point.validate_of_class("temperature")
        boiling_point.validate_of_class("temperature")
        validate_of_type(exist_weight, Number, "exist_weight")
        validate_of_type(concentration_weight, Probability, "concentration_weight")

        self.name = name
        self.symbol = symbol
        self.melting_point = melting_point.convert("°K")
        self.boiling_point = boiling_point.convert("°K")
        self.exist_weight = exist_weight
        self.concentration_weight = concentration_weight

    @staticmethod
    def from_dict(data: dict) -> 'Molecule':
        retrieved_data = {
            "name": data.get("name", None),
            "symbol": data.get("symbol", None),
            "melting_point": None,
            "boiling_point": None,
            "exist_weight": data.get("exist_weight", None),
            "concentration_weight": None
        }

        melting_point = data.get("melting_point", None)
        if isinstance(melting_point, (str, dict)):
            retrieved_data["melting_point"] = UnitValue.from_any(melting_point)
        boiling_point = data.get("boiling_point", None)
        if isinstance(boiling_point, (str, dict)):
            retrieved_data["boiling_point"] = UnitValue.from_any(boiling_point)
        concentration_weight = data.get("concentration_weight", None)
        if isinstance(concentration_weight, dict):
            retrieved_data["concentration_weight"] = Probability.create(concentration_weight)

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
    
    def get_exist_weight(self) -> int:
        return self.exist_weight
    
    def get_concentration_weight(self) -> int:
        return int(self.concentration_weight.generate())
    
    def get_state_at(self, temperature: UnitValue) -> AggregateState:
        temperature.validate_of_class("temperature")
        current_temp = temperature.convert("°K").get_value()

        if current_temp < self.melting_point.get_value():
            return AggregateState.SOLID
        
        if current_temp > self.boiling_point.get_value():
            return AggregateState.GASEOUS
        
        return AggregateState.LIQUID