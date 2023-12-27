import random
from typing import Any

class RandomSelector():
    def __init__(self) -> None:
        return
    
    def __str__(self) -> str:
        return ""
    
    @staticmethod
    def create() -> 'RandomSelector':
        return RandomSelector()

    def select(self):
        return 0

class MinMaxSelector(RandomSelector):
    def __init__(self, min: float, max: float) -> None:
        self.min = min
        self.max = max

    def __str__(self) -> str:
        return f"(min:{self.min}-max:{self.max})"

    @staticmethod
    def create(data: dict) -> 'MinMaxSelector':
        min = data.get("min", 0)
        max = data.get("max", 0)
        return MinMaxSelector(min=min, max=max)

    def select(self):
        return random.uniform(self.min, self.max)
    
class WeightedSelector(RandomSelector):
    def __init__(self, weights: list[float], values: list) -> None:
        if len(weights) != len(values):
            raise ValueError("An error occured while initializing weighted selector: the amount of weights and values has to be the same.")
        self.weights = weights
        self.values = values
        self.total_weight = sum(weights)

    def __str__(self) -> str:
        value_weight_map = {str(value): str(weight) for value, weight in zip(self.values, self.weights)}
        return '\n'.join([f"{value}: {weight}" for value, weight in value_weight_map.items()])

    @staticmethod
    def create(data: dict) -> 'WeightedSelector':
        weights = data.get("weights", [])
        values = data.get("values", [])

        if len(weights) != len(values):
            raise ValueError("An error occured while initializing weighted selector: the amount of weights and values has to be the same.")
        for i, value in enumerate(values):
            if isinstance(value, dict):
                values[i] = MinMaxSelector.create(data=value)
            elif isinstance(value, list):
                values[i] = ListSelector.create(data=value)
        return WeightedSelector(weights=weights, values=values)
    
    def select(self):
        result = None
        random_value = random.uniform(0, self.total_weight)
        for weight, value in zip(self.weights, self.values):
            random_value -= weight
            if random_value <= 0:
                result = value
                break

        if result is None:
            raise RuntimeError("Weighted random selector did not yield any value.")
        if isinstance(result, RandomSelector):
            return result.select()
        return result
    
class ListSelector(RandomSelector):
    def __init__(self, values: list) -> None:
        self.values = values

    def __str__(self) -> str:
        return f"({", ".join([str(value) for value in self.values])})"
    
    @staticmethod
    def create(data: list) -> 'ListSelector':
        if len(data) == 0:
            data = [None]
        return ListSelector(values=data)
    
    def select(self):
        return random.choice(self.values)
    
class SingleSelector(RandomSelector):
    def __init__(self, value = None) -> None:
        self.value = value

    def __str__(self) -> str:
        return str(self.value)
    
    @staticmethod
    def create(data = None) -> 'SingleSelector':
        return SingleSelector(value=data)
    
    def select(self):
        return self.value
    
class Probability():
    def __init__(self, selector: RandomSelector) -> None:
        self.selector = selector

    def __str__(self) -> str:
        return str(self.selector)

    @staticmethod
    def create(data) -> 'Probability':
        if isinstance(data, list):
            selector = ListSelector(data)
        elif isinstance(data, dict):
            if data.get("min") is not None or data.get("max") is not None:
                selector = MinMaxSelector.create(data)
            else:
                selector = WeightedSelector.create(data)
        else:
            selector = SingleSelector.create(data)
        return Probability(selector=selector)
    
    def generate(self) -> Any:
        return self.selector.select()