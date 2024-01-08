from typing import Optional
from src.space_ship.ship_system import ShipSystem
from src.space_ship.upgrade_model import UpgradeModel

class HullSystem(ShipSystem):
    NAME = "hull"

    def __init__(self, upgrade_model: UpgradeModel, max_hp: int, hp: Optional[int] = None, subscriptions: Optional[dict] = None) -> None:
        super().__init__(upgrade_model, max_hp, 0, hp, subscriptions)