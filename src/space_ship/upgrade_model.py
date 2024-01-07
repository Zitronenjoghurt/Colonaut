from src.utils.file_operations import file_to_dict, files_in_directory, construct_path

UPGRADE_MODELS_FILE_PATH = construct_path("src/data/system_models/")

class UpgradeModel():
    def __init__(self, system_name: str, model_name: str, upgrades: dict[str, list[tuple[int, int]]]) -> None:
        self.system_name = system_name
        self.model_name = model_name
        self.upgrades = upgrades
    
    @staticmethod
    def from_dict(system_name: str, model_name: str, data: dict) -> 'UpgradeModel':
        upgrades = {}
        try:
            for property_name, property_data in data.items():
                upgrades[property_name] = [(upgrade.get("value", 0), upgrade.get("cost", 0)) for upgrade in property_data]
        except Exception as e:
            raise RuntimeError(f"An error occured while trying to load model {model_name} of system {system_name}: {e}")
        return UpgradeModel(system_name=system_name, model_name=model_name, upgrades=upgrades)

    def get_entry(self, property: str, level: int) -> dict[str, int]:
        property_upgrades = self.upgrades.get(property, None)
        if property_upgrades is None:
            raise RuntimeError(f"Tried to access level {level} of property {property}, but the property does not exist in the {self.model_name} model of system {self.system_name}")
        
        if level > len(property_upgrades):
            raise RuntimeError(f"Tried to access level {level} of property {property}, but the max level is {len(property_upgrades)} in model {self.model_name} of system {self.system_name}")
        
        value = property_upgrades[level-1][0]
        cost = property_upgrades[level-1][1]
        return {'value': value, 'cost': cost}

    def get_level_value(self, property: str, level: int) -> int:
        entry = self.get_entry(property=property, level=level)
        value = entry.get("value", None)
        if value is None:
            raise RuntimeError(f"An error occured while retrieving the value of property {property} at level {level} of model {self.model_name} of system {self.system_name}")
        return value
    
    def get_value_level(self, property: str, value: int) -> int:
        property_levels = self.upgrades.get(property, None)
        if property_levels is None:
            raise ValueError(f"Property {property} was not found in system {self.system_name} model {self.model_name}")
        for i, entry in enumerate(property_levels):
            entry_value = entry[0]
            if value == entry_value:
                return i+1
        raise ValueError(f"No specified value {value} for property {property} in system {self.system_name} model {self.model_name}")
    
    def get_level_cost(self, property: str, level: int) -> int:
        entry = self.get_entry(property=property, level=level)
        value = entry.get("cost", None)
        if value is None:
            raise RuntimeError(f"An error occured while retrieving the cost of property {property} at level {level} of model {self.model_name} of system {self.system_name}")
        return value
    
    def get_upgrade_difference(self, property: str, current_level: int) -> int:
        current_value = self.get_level_value(property=property, level=current_level)
        next_value = self.get_level_value(property=property, level=current_level+1)
        return round(next_value-current_value, 1)
    
    def get_initial_value(self, property: str) -> int:
        return self.get_level_value(property=property, level=1)
    
    def get_upgrades(self) -> dict[str, list[tuple[int, int]]]:
        return self.upgrades
    
    def is_max_level(self, property: str, level: int) -> bool:
        property_levels = self.upgrades.get(property, None)
        if property_levels is None:
            raise ValueError(f"Property {property} was not found in system {self.system_name} model {self.model_name}")
        if level == len(property_levels):
            return True
        return False
    
    def get_next_value(self, property: str, value: int) -> int:
        level = self.get_value_level(property=property, value=value)
        next_value = self.get_level_value(property=property, level=level+1)
        return next_value
    
    def get_upgrade_option(self, property: str, value: int) -> dict:
        current_level = self.get_value_level(property=property, value=value)
        is_max = self.is_max_level(property=property, level=current_level)

        if not is_max:
            difference = "+" + str(self.get_upgrade_difference(property=property, current_level=current_level))
        else:
            difference = "MAX"
        
        if not is_max:
            cost = self.get_level_cost(property=property, level=current_level+1)
        else:
            cost = 0

        return {"property": property, "difference": difference, "cost": str(cost)}
    
class UpgradeModelLibrary():
    _instance = None

    def __init__(self) -> None:
        if UpgradeModelLibrary._instance is not None:
            raise RuntimeError("Tried to initialize multiple instances of UpgradeModelLibrary.")
        
        self.systems = {}
        for file in files_in_directory(UPGRADE_MODELS_FILE_PATH, 'json'):
            system_name = file[:-5]
            self.systems[system_name] = self._load_models(system_name)
    
    @staticmethod
    def _load_models(system_name: str) -> dict[str, UpgradeModel]:
        path = UPGRADE_MODELS_FILE_PATH+system_name+'.json'
        models = file_to_dict(path)
        
        data = {}
        for model_name, model_data in models.items():
            data[model_name] = UpgradeModel.from_dict(system_name, model_name, model_data)
        return data

    @staticmethod
    def get_instance() -> 'UpgradeModelLibrary':
        if UpgradeModelLibrary._instance is None:
            UpgradeModelLibrary._instance = UpgradeModelLibrary()
        return UpgradeModelLibrary._instance
    
    def get_model(self, system_name: str, model_name: str = 'standard') -> UpgradeModel:
        system_models = self.systems.get(system_name, None)
        if system_models is None:
            raise ValueError(f"System {system_name} has no specified models")

        model = system_models.get(model_name, None)
        if not isinstance(model, UpgradeModel):
            raise ValueError(f"Model {model_name} not found in system {system_name}")
        
        return model