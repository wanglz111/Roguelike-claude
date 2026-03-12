from dataclasses import dataclass
from typing import Optional


@dataclass
class Monster:
    name: str
    hp: int
    attack: int
    defense: int
    exp_reward: int
    gold_reward: int
    drop_item: Optional[str] = None
