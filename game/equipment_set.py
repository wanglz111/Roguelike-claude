from dataclasses import dataclass
from typing import Union, Dict

from game.i18n import t


@dataclass
class EquipmentSet:
    set_id: str
    name: Union[str, Dict[str, str]]
    description: Union[str, Dict[str, str]]
    items: list[str]  # List of item names (English)
    bonus_attack: int = 0
    bonus_defense: int = 0
    bonus_hp: int = 0

    def get_name(self) -> str:
        """Get localized name."""
        return t(self.name)

    def get_description(self) -> str:
        """Get localized description."""
        return t(self.description)
