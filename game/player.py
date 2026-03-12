from dataclasses import dataclass, field
from typing import Set

from game.i18n import t


@dataclass
class Player:
    name: str
    max_hp: int = 30
    hp: int = 30
    max_mp: int = 20
    mp: int = 20
    attack: int = 8
    defense: int = 3
    level: int = 1
    exp: int = 0
    gold: int = 0
    inventory: list = field(default_factory=list)
    weapon: object = None
    armor: object = None
    accessory: object = None
    player_class: str = "rogue"  # Default class
    hp_per_level: int = 6
    mp_per_level: int = 5
    attack_per_level: int = 2
    defense_per_level: int = 1
    unlocked_achievements: Set[str] = field(default_factory=set)  # Set of achievement IDs
    # Achievement tracking stats
    monsters_killed: int = 0
    bosses_killed: int = 0
    skills_used: int = 0
    items_purchased: int = 0

    @property
    def exp_to_next_level(self) -> int:
        return 10 + (self.level - 1) * 8

    @property
    def is_alive(self) -> bool:
        return self.hp > 0

    @property
    def total_attack(self) -> int:
        bonus = 0
        if self.weapon:
            bonus += self.weapon.effective_bonus_attack
        if self.armor:
            bonus += self.armor.effective_bonus_attack
        if self.accessory:
            bonus += self.accessory.effective_bonus_attack
        return self.attack + bonus

    @property
    def total_defense(self) -> int:
        bonus = 0
        if self.weapon:
            bonus += self.weapon.effective_bonus_defense
        if self.armor:
            bonus += self.armor.effective_bonus_defense
        if self.accessory:
            bonus += self.accessory.effective_bonus_defense
        return self.defense + bonus

    @property
    def total_max_hp(self) -> int:
        bonus = 0
        if self.weapon:
            bonus += self.weapon.effective_bonus_hp
        if self.armor:
            bonus += self.armor.effective_bonus_hp
        if self.accessory:
            bonus += self.accessory.effective_bonus_hp
        return self.max_hp + bonus

    @property
    def total_max_mp(self) -> int:
        """Total max MP (for consistency with total_max_hp)."""
        return self.max_mp

    def unlock_achievement(self, achievement_id: str) -> bool:
        """Unlock an achievement. Returns True if newly unlocked, False if already unlocked."""
        if achievement_id in self.unlocked_achievements:
            return False
        self.unlocked_achievements.add(achievement_id)
        return True

    def has_achievement(self, achievement_id: str) -> bool:
        """Check if an achievement is unlocked."""
        return achievement_id in self.unlocked_achievements

    def add_item(self, item) -> str:
        self.inventory.append(item)
        return t({"en": f"You obtained {item.get_name()}!", "zh": f"你获得了{item.get_name()}！"})

    def equip_item(self, index: int) -> str:
        if index < 0 or index >= len(self.inventory):
            return t({"en": "Invalid item.", "zh": "无效的物品。"})
        item = self.inventory[index]
        if item.item_type != "equipment":
            return t({"en": "This item cannot be equipped.", "zh": "该物品无法装备。"})

        old_item = None
        if item.equipment_slot == "weapon":
            old_item = self.weapon
            self.weapon = item
        elif item.equipment_slot == "armor":
            old_item = self.armor
            self.armor = item
        elif item.equipment_slot == "accessory":
            old_item = self.accessory
            self.accessory = item
        else:
            return t({"en": "Unknown equipment slot.", "zh": "未知的装备槽。"})

        self.inventory.pop(index)
        if old_item:
            self.inventory.append(old_item)
            return t({"en": f"Equipped {item.get_name()}. Unequipped {old_item.get_name()}.", "zh": f"装备了{item.get_name()}。卸下了{old_item.get_name()}。"})
        return t({"en": f"Equipped {item.get_name()}.", "zh": f"装备了{item.get_name()}。"})

    def use_item(self, index: int) -> str:
        if index < 0 or index >= len(self.inventory):
            return t({"en": "Invalid item.", "zh": "无效的物品。"})
        item = self.inventory.pop(index)
        if item.effect_type == "heal":
            old_hp = self.hp
            self.hp = min(self.total_max_hp, self.hp + item.effect_value)
            healed = self.hp - old_hp
            return t({"en": f"Used {item.get_name()}. Restored {healed} HP.", "zh": f"使用了{item.get_name()}。恢复了{healed}点生命值。"})
        elif item.effect_type == "restore_mp":
            old_mp = self.mp
            self.mp = min(self.total_max_mp, self.mp + item.effect_value)
            restored = self.mp - old_mp
            return t({"en": f"Used {item.get_name()}. Restored {restored} MP.", "zh": f"使用了{item.get_name()}。恢复了{restored}点魔力值。"})
        return t({"en": f"Used {item.get_name()}.", "zh": f"使用了{item.get_name()}。"})

    def gain_rewards(self, exp: int, gold: int) -> list[str]:
        self.exp += exp
        self.gold += gold
        messages = [t({"en": f"You gain {exp} EXP and {gold} gold.", "zh": f"你获得了{exp}点经验和{gold}金币。"})]
        while self.exp >= self.exp_to_next_level:
            threshold = self.exp_to_next_level
            self.exp -= threshold
            self.level += 1
            self.max_hp += self.hp_per_level
            self.max_mp += self.mp_per_level
            self.attack += self.attack_per_level
            self.defense += self.defense_per_level
            self.hp = self.max_hp
            self.mp = self.max_mp
            messages.append(
                t({"en": f"Level up! You reached level {self.level}. HP and MP fully restored.", "zh": f"升级了！你达到了{self.level}级。生命值和魔法值已完全恢复。"})
            )
        return messages

    def apply_event_effect(self, effect_type: str, effect_value: int) -> str:
        """Apply an event effect to the player.

        Args:
            effect_type: Type of effect (heal, damage, gold, trade_heal, boost_attack, etc.)
            effect_value: Value of the effect

        Returns:
            Additional message if any (e.g., insufficient gold)
        """
        if effect_type == "heal":
            old_hp = self.hp
            self.hp = min(self.total_max_hp, self.hp + effect_value)
            healed = self.hp - old_hp
            if healed > 0:
                return ""
            return t({"en": " (Already at full HP)", "zh": "（生命值已满）"})

        elif effect_type == "damage":
            self.hp = max(0, self.hp - effect_value)
            return ""

        elif effect_type == "gold":
            self.gold += effect_value
            return ""

        elif effect_type == "gold_with_hp_cost":
            # Give gold but cost HP (e.g., helping wounded adventurer)
            hp_cost = 10
            self.hp = max(0, self.hp - hp_cost)
            self.gold += effect_value
            return ""

        elif effect_type == "trade_heal":
            cost = 20
            if self.gold >= cost:
                self.gold -= cost
                old_hp = self.hp
                self.hp = min(self.total_max_hp, self.hp + effect_value)
                return ""
            else:
                return t({"en": " (Not enough gold!)", "zh": "（金币不足！）"})

        elif effect_type == "trade_gold_for_heal":
            cost = 50
            if self.gold >= cost:
                self.gold -= cost
                old_hp = self.hp
                self.hp = min(self.total_max_hp, self.hp + effect_value)
                return ""
            else:
                return t({"en": " (Not enough gold!)", "zh": "（金币不足！）"})

        elif effect_type == "boost_attack":
            # Permanently increase attack
            self.attack += effect_value
            return ""

        elif effect_type == "boost_defense":
            # Permanently increase defense
            self.defense += effect_value
            return ""

        elif effect_type == "boost_max_hp":
            # Permanently increase max HP and heal to new max
            self.max_hp += effect_value
            self.hp = min(self.total_max_hp, self.hp + effect_value)
            return ""

        elif effect_type == "trade_boost_attack":
            # Pay gold for permanent attack boost
            cost = 60
            if self.gold >= cost:
                self.gold -= cost
                self.attack += effect_value
                return ""
            else:
                return t({"en": " (Not enough gold!)", "zh": "（金币不足！）"})

        elif effect_type == "nothing":
            return ""

        return ""
