import json
from dataclasses import dataclass
from game.i18n import t


@dataclass
class StatusEffect:
    """Represents a status effect that can be applied to a player or monster."""
    effect_id: str
    name: dict
    description: dict
    effect_type: str  # poison, burn, freeze, bleed, regen
    damage_per_turn: int = 0  # Damage dealt each turn (for poison, burn, bleed)
    heal_per_turn: int = 0  # Healing each turn (for regen)
    duration: int = 3  # Number of turns the effect lasts
    attack_modifier: float = 1.0  # Multiplier for attack (e.g., 0.5 for freeze)
    defense_modifier: float = 1.0  # Multiplier for defense

    def get_name(self) -> str:
        return t(self.name)

    def get_description(self) -> str:
        return t(self.description)


@dataclass
class ActiveStatusEffect:
    """Represents an active status effect on a player or monster."""
    effect: StatusEffect
    remaining_turns: int

    def tick(self) -> int:
        """Process one turn of the status effect. Returns damage dealt (negative for healing)."""
        self.remaining_turns -= 1
        if self.effect.damage_per_turn > 0:
            return self.effect.damage_per_turn
        elif self.effect.heal_per_turn > 0:
            return -self.effect.heal_per_turn
        return 0

    def is_expired(self) -> bool:
        """Check if the status effect has expired."""
        return self.remaining_turns <= 0


def load_status_effects() -> dict[str, StatusEffect]:
    """Load all status effects from JSON file."""
    with open("content/status_effects.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return {
        effect_id: StatusEffect(
            effect_id=effect_id,
            name=effect_data["name"],
            description=effect_data["description"],
            effect_type=effect_data["effect_type"],
            damage_per_turn=effect_data.get("damage_per_turn", 0),
            heal_per_turn=effect_data.get("heal_per_turn", 0),
            duration=effect_data.get("duration", 3),
            attack_modifier=effect_data.get("attack_modifier", 1.0),
            defense_modifier=effect_data.get("defense_modifier", 1.0),
        )
        for effect_id, effect_data in data.items()
    }
