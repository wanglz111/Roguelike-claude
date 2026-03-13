from dataclasses import dataclass
from typing import Optional, Union, Dict

from game.i18n import t


@dataclass
class Monster:
    name: Union[str, Dict[str, str]]
    hp: int
    attack: int
    defense: int
    exp_reward: int
    gold_reward: int
    drop_item: Optional[str] = None
    is_boss: bool = False
    special_ability: Optional[str] = None
    status_effect_id: Optional[str] = None
    lifesteal_percent: Optional[int] = None

    def get_name(self) -> str:
        """Get localized name."""
        return t(self.name)
