from dataclasses import dataclass
from typing import Union, Dict

from game.i18n import t


@dataclass
class Item:
    name: Union[str, Dict[str, str]]
    item_type: str  # "consumable", "equipment", etc.
    effect_type: str  # "heal", "buff_attack", etc.
    effect_value: int
    description: Union[str, Dict[str, str]]
    equipment_slot: str = ""  # "weapon", "armor", "" for non-equipment
    bonus_attack: int = 0
    bonus_defense: int = 0
    bonus_hp: int = 0

    def get_name(self) -> str:
        """Get localized name."""
        return t(self.name)

    def get_description(self) -> str:
        """Get localized description."""
        return t(self.description)
