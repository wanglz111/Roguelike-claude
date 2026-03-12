from dataclasses import dataclass


@dataclass
class Item:
    name: str
    item_type: str  # "consumable", "equipment", etc.
    effect_type: str  # "heal", "buff_attack", etc.
    effect_value: int
    description: str
