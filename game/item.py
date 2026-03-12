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
    rarity: str = "common"  # "common", "rare", "epic", "legendary"

    def get_name(self) -> str:
        """Get localized name."""
        return t(self.name)

    def get_description(self) -> str:
        """Get localized description."""
        return t(self.description)

    def get_rarity_multiplier(self) -> float:
        """Get stat multiplier based on rarity."""
        multipliers = {"common": 1.0, "rare": 1.3, "epic": 1.6, "legendary": 2.0}
        return multipliers.get(self.rarity, 1.0)

    @property
    def effective_bonus_attack(self) -> int:
        """Get attack bonus with rarity multiplier applied."""
        return int(self.bonus_attack * self.get_rarity_multiplier())

    @property
    def effective_bonus_defense(self) -> int:
        """Get defense bonus with rarity multiplier applied."""
        return int(self.bonus_defense * self.get_rarity_multiplier())

    @property
    def effective_bonus_hp(self) -> int:
        """Get HP bonus with rarity multiplier applied."""
        return int(self.bonus_hp * self.get_rarity_multiplier())
