import json
from dataclasses import dataclass
from pathlib import Path

from game.i18n import t


@dataclass
class PlayerClass:
    """Represents a player class with base stats and growth rates."""
    class_id: str
    name: dict
    description: dict
    base_hp: int
    base_mp: int
    base_attack: int
    base_defense: int
    hp_per_level: int
    mp_per_level: int
    attack_per_level: int
    defense_per_level: int

    def get_name(self) -> str:
        return t(self.name)

    def get_description(self) -> str:
        return t(self.description)


def load_classes() -> dict[str, PlayerClass]:
    """Load all player classes from classes.json."""
    path = Path(__file__).parent.parent / "content" / "classes.json"
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    classes = {}
    for class_id, class_data in data.items():
        classes[class_id] = PlayerClass(
            class_id=class_id,
            name=class_data["name"],
            description=class_data["description"],
            base_hp=class_data["base_hp"],
            base_mp=class_data["base_mp"],
            base_attack=class_data["base_attack"],
            base_defense=class_data["base_defense"],
            hp_per_level=class_data["hp_per_level"],
            mp_per_level=class_data["mp_per_level"],
            attack_per_level=class_data["attack_per_level"],
            defense_per_level=class_data["defense_per_level"],
        )
    return classes
