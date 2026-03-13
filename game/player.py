from dataclasses import dataclass, field
from typing import Set, List, TYPE_CHECKING

from game.i18n import t

if TYPE_CHECKING:
    from game.status_effect import ActiveStatusEffect


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
    consumables_used: int = 0
    status_effects_applied: int = 0
    events_encountered: int = 0
    completed_classes: Set[str] = field(default_factory=set)  # Set of class names that completed the dungeon
    equipped_sets: Set[str] = field(default_factory=set)  # Set of equipment set IDs that have been equipped
    # Status effects
    status_effects: List = field(default_factory=list)  # List of ActiveStatusEffect

    @property
    def exp_to_next_level(self) -> int:
        return 10 + (self.level - 1) * 8

    @property
    def is_alive(self) -> bool:
        return self.hp > 0

    def get_active_set_bonus(self):
        """Get equipment set bonus if wearing a complete set."""
        if not self.weapon and not self.armor and not self.accessory:
            return None

        from game.floor import load_equipment_sets
        equipment_sets = load_equipment_sets()

        equipped_names = set()
        if self.weapon:
            name = self.weapon.name if isinstance(self.weapon.name, str) else self.weapon.name.get("en", "")
            equipped_names.add(name)
        if self.armor:
            name = self.armor.name if isinstance(self.armor.name, str) else self.armor.name.get("en", "")
            equipped_names.add(name)
        if self.accessory:
            name = self.accessory.name if isinstance(self.accessory.name, str) else self.accessory.name.get("en", "")
            equipped_names.add(name)

        for eq_set in equipment_sets:
            if all(item_name in equipped_names for item_name in eq_set.items):
                return eq_set
        return None

    @property
    def total_attack(self) -> int:
        bonus = 0
        if self.weapon:
            bonus += self.weapon.effective_bonus_attack
        if self.armor:
            bonus += self.armor.effective_bonus_attack
        if self.accessory:
            bonus += self.accessory.effective_bonus_attack

        # Add set bonus
        active_set = self.get_active_set_bonus()
        if active_set:
            bonus += active_set.bonus_attack

        base_attack = self.attack + bonus

        # Apply status effect modifiers
        for active_effect in self.status_effects:
            base_attack = int(base_attack * active_effect.effect.attack_modifier)

        return base_attack

    @property
    def total_defense(self) -> int:
        bonus = 0
        if self.weapon:
            bonus += self.weapon.effective_bonus_defense
        if self.armor:
            bonus += self.armor.effective_bonus_defense
        if self.accessory:
            bonus += self.accessory.effective_bonus_defense

        # Add set bonus
        active_set = self.get_active_set_bonus()
        if active_set:
            bonus += active_set.bonus_defense

        base_defense = self.defense + bonus

        # Apply status effect modifiers
        for active_effect in self.status_effects:
            base_defense = int(base_defense * active_effect.effect.defense_modifier)

        return base_defense

    @property
    def total_max_hp(self) -> int:
        bonus = 0
        if self.weapon:
            bonus += self.weapon.effective_bonus_hp
        if self.armor:
            bonus += self.armor.effective_bonus_hp
        if self.accessory:
            bonus += self.accessory.effective_bonus_hp

        # Add set bonus
        active_set = self.get_active_set_bonus()
        if active_set:
            bonus += active_set.bonus_hp

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

        # Track consumable usage for achievements
        self.consumables_used += 1

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
        elif item.effect_type == "restore_both":
            old_hp = self.hp
            old_mp = self.mp
            self.hp = min(self.total_max_hp, self.hp + item.effect_value)
            self.mp = min(self.total_max_mp, self.mp + item.effect_value)
            healed = self.hp - old_hp
            restored = self.mp - old_mp
            return t({"en": f"Used {item.get_name()}. Restored {healed} HP and {restored} MP.", "zh": f"使用了{item.get_name()}。恢复了{healed}点生命值和{restored}点魔力值。"})
        elif item.effect_type == "cure_status":
            count = len(self.status_effects)
            self.clear_status_effects()
            if count > 0:
                return t({"en": f"Used {item.get_name()}. Removed {count} status effect(s).", "zh": f"使用了{item.get_name()}。移除了{count}个状态效果。"})
            return t({"en": f"Used {item.get_name()}. No status effects to remove.", "zh": f"使用了{item.get_name()}。没有状态效果需要移除。"})
        elif item.effect_type == "full_restore":
            self.hp = self.total_max_hp
            self.mp = self.total_max_mp
            return t({"en": f"Used {item.get_name()}. HP and MP fully restored!", "zh": f"使用了{item.get_name()}。生命值和魔力值已完全恢复！"})
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

        elif effect_type == "trade_boost_defense":
            # Pay gold for permanent defense boost
            cost = 40
            if self.gold >= cost:
                self.gold -= cost
                self.defense += effect_value
                return ""
            else:
                return t({"en": " (Not enough gold!)", "zh": "（金币不足！）"})

        elif effect_type == "trade_boost_max_hp":
            # Pay gold for permanent max HP boost
            cost = 60
            if self.gold >= cost:
                self.gold -= cost
                self.max_hp += effect_value
                self.hp = min(self.total_max_hp, self.hp + effect_value)
                return ""
            else:
                return t({"en": " (Not enough gold!)", "zh": "（金币不足！）"})

        elif effect_type == "trade_hp_for_attack":
            # Sacrifice HP for permanent attack boost
            hp_cost = 30
            self.hp = max(1, self.hp - hp_cost)
            self.attack += effect_value
            return ""

        elif effect_type == "risky_gold":
            # 60% chance to get gold, 40% chance to take damage
            import random
            if random.random() < 0.6:
                self.gold += effect_value
                return t({"en": " Success! You got the treasure!", "zh": " 成功！你得到了宝藏！"})
            else:
                self.hp = max(0, self.hp - 25)
                return t({"en": " The dragon wakes! You take 25 damage!", "zh": " 巨龙醒了！你受到25点伤害！"})

        elif effect_type == "wish":
            # Pay gold for random beneficial effect
            cost = 30
            if self.gold >= cost:
                self.gold -= cost
                import random
                wish_type = random.choice(["heal", "attack", "defense", "max_hp"])
                if wish_type == "heal":
                    old_hp = self.hp
                    self.hp = min(self.total_max_hp, self.hp + 30)
                    healed = self.hp - old_hp
                    return t({"en": f" Granted +{healed} HP!", "zh": f" 获得+{healed}生命值！"})
                elif wish_type == "attack":
                    self.attack += 2
                    return t({"en": " Granted +2 attack!", "zh": " 获得+2攻击！"})
                elif wish_type == "defense":
                    self.defense += 2
                    return t({"en": " Granted +2 defense!", "zh": " 获得+2防御！"})
                else:  # max_hp
                    self.max_hp += 10
                    self.hp = min(self.total_max_hp, self.hp + 10)
                    return t({"en": " Granted +10 max HP!", "zh": " 获得+10最大生命值！"})
            else:
                return t({"en": " (Not enough gold!)", "zh": "（金币不足！）"})

        elif effect_type == "search_battlefield":
            # 60% chance to find gold, 40% chance to find nothing
            import random
            if random.random() < 0.6:
                self.gold += effect_value
                return t({"en": " You found salvageable equipment!", "zh": " 你找到了可用的装备！"})
            else:
                return t({"en": " You found nothing useful.", "zh": " 你没有找到有用的东西。"})

        elif effect_type == "nothing":
            return ""

        return ""

    def add_status_effect(self, status_effect: 'ActiveStatusEffect') -> str:
        """Add a status effect to the player.

        Args:
            status_effect: The ActiveStatusEffect to add

        Returns:
            Message describing the effect applied
        """
        # Check if the same effect type already exists
        for existing in self.status_effects:
            if existing.effect.effect_id == status_effect.effect.effect_id:
                # Refresh duration instead of stacking
                existing.remaining_turns = status_effect.remaining_turns
                return t({"en": f"{status_effect.effect.get_name()} effect refreshed!",
                         "zh": f"{status_effect.effect.get_name()}效果已刷新！"})

        self.status_effects.append(status_effect)
        return t({"en": f"You are afflicted with {status_effect.effect.get_name()}!",
                 "zh": f"你受到了{status_effect.effect.get_name()}效果！"})

    def process_status_effects(self) -> list[str]:
        """Process all active status effects for one turn.

        Returns:
            List of messages describing what happened
        """
        messages = []
        effects_to_remove = []

        for active_effect in self.status_effects:
            damage = active_effect.tick()

            if damage > 0:
                # Damage effect
                self.hp = max(0, self.hp - damage)
                messages.append(t({
                    "en": f"{active_effect.effect.get_name()} deals {damage} damage!",
                    "zh": f"{active_effect.effect.get_name()}造成了{damage}点伤害！"
                }))
            elif damage < 0:
                # Healing effect
                heal_amount = -damage
                old_hp = self.hp
                self.hp = min(self.total_max_hp, self.hp + heal_amount)
                actual_heal = self.hp - old_hp
                if actual_heal > 0:
                    messages.append(t({
                        "en": f"{active_effect.effect.get_name()} restores {actual_heal} HP!",
                        "zh": f"{active_effect.effect.get_name()}恢复了{actual_heal}点生命值！"
                    }))

            if active_effect.is_expired():
                effects_to_remove.append(active_effect)
                messages.append(t({
                    "en": f"{active_effect.effect.get_name()} has worn off.",
                    "zh": f"{active_effect.effect.get_name()}效果已消失。"
                }))

        # Remove expired effects
        for effect in effects_to_remove:
            self.status_effects.remove(effect)

        return messages

    def clear_status_effects(self):
        """Clear all status effects (e.g., on level up or using special items)."""
        self.status_effects.clear()
