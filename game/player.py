from dataclasses import dataclass, field


@dataclass
class Player:
    name: str
    max_hp: int = 30
    hp: int = 30
    attack: int = 8
    defense: int = 3
    level: int = 1
    exp: int = 0
    gold: int = 0
    inventory: list = field(default_factory=list)

    @property
    def exp_to_next_level(self) -> int:
        return 10 + (self.level - 1) * 8

    @property
    def is_alive(self) -> bool:
        return self.hp > 0

    def add_item(self, item) -> str:
        self.inventory.append(item)
        return f"You obtained {item.name}!"

    def use_item(self, index: int) -> str:
        if index < 0 or index >= len(self.inventory):
            return "Invalid item."
        item = self.inventory.pop(index)
        if item.effect_type == "heal":
            old_hp = self.hp
            self.hp = min(self.max_hp, self.hp + item.effect_value)
            healed = self.hp - old_hp
            return f"Used {item.name}. Restored {healed} HP."
        return f"Used {item.name}."

    def gain_rewards(self, exp: int, gold: int) -> list[str]:
        self.exp += exp
        self.gold += gold
        messages = [f"You gain {exp} EXP and {gold} gold."]
        while self.exp >= self.exp_to_next_level:
            threshold = self.exp_to_next_level
            self.exp -= threshold
            self.level += 1
            self.max_hp += 6
            self.attack += 2
            self.defense += 1
            self.hp = self.max_hp
            messages.append(
                f"Level up! You reached level {self.level}. HP fully restored."
            )
        return messages
