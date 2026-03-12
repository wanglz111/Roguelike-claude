"""Achievement checking logic."""

from typing import List, Tuple
from game.player import Player
from game.achievement import Achievement, get_achievement_by_id
from game.i18n import t


def check_achievements(player: Player, achievements: List[Achievement], trigger: str, **kwargs) -> List[Tuple[str, Achievement]]:
    """Check for newly unlocked achievements based on a trigger event.

    Args:
        player: The player object
        achievements: List of all achievements
        trigger: The event that triggered the check (e.g., "monster_killed", "floor_reached")
        **kwargs: Additional context (e.g., monster_name, floor_number, is_boss)

    Returns:
        List of tuples (achievement_id, Achievement) for newly unlocked achievements
    """
    newly_unlocked = []

    if trigger == "monster_killed":
        # First Blood
        if player.monsters_killed == 1:
            if player.unlock_achievement("first_blood"):
                newly_unlocked.append(("first_blood", get_achievement_by_id(achievements, "first_blood")))

        # Boss achievements
        if kwargs.get("is_boss", False):
            if player.bosses_killed == 1:
                if player.unlock_achievement("boss_slayer"):
                    newly_unlocked.append(("boss_slayer", get_achievement_by_id(achievements, "boss_slayer")))

            # Specific boss achievements
            monster_name = kwargs.get("monster_name", "")
            boss_achievements = {
                "Goblin Warlord": "goblin_warlord_defeated",
                "哥布林军阀": "goblin_warlord_defeated",
                "Lich King": "lich_king_defeated",
                "巫妖王": "lich_king_defeated",
                "Ancient Dragon": "ancient_dragon_defeated",
                "远古巨龙": "ancient_dragon_defeated",
                "Demon Lord": "demon_lord_defeated",
                "魔王": "demon_lord_defeated"
            }
            if monster_name in boss_achievements:
                ach_id = boss_achievements[monster_name]
                if player.unlock_achievement(ach_id):
                    newly_unlocked.append((ach_id, get_achievement_by_id(achievements, ach_id)))

    elif trigger == "floor_reached":
        floor = kwargs.get("floor", 0)
        floor_achievements = {
            5: "floor_5",
            10: "floor_10",
            15: "floor_15",
            20: "floor_20"
        }
        if floor in floor_achievements:
            ach_id = floor_achievements[floor]
            if player.unlock_achievement(ach_id):
                newly_unlocked.append((ach_id, get_achievement_by_id(achievements, ach_id)))

        # Completion achievement
        if floor > 20:
            if player.unlock_achievement("first_completion"):
                newly_unlocked.append(("first_completion", get_achievement_by_id(achievements, "first_completion")))

    elif trigger == "level_up":
        level = player.level
        if level == 10:
            if player.unlock_achievement("level_10"):
                newly_unlocked.append(("level_10", get_achievement_by_id(achievements, "level_10")))
        elif level == 20:
            if player.unlock_achievement("level_20"):
                newly_unlocked.append(("level_20", get_achievement_by_id(achievements, "level_20")))

    elif trigger == "equipment_equipped":
        # First equipment
        if (player.weapon or player.armor or player.accessory):
            if player.unlock_achievement("first_equipment"):
                newly_unlocked.append(("first_equipment", get_achievement_by_id(achievements, "first_equipment")))

        # Full equipment
        if player.weapon and player.armor and player.accessory:
            if player.unlock_achievement("full_equipment"):
                newly_unlocked.append(("full_equipment", get_achievement_by_id(achievements, "full_equipment")))

        # Rarity achievements
        item = kwargs.get("item", None)
        if item and hasattr(item, "rarity"):
            if item.rarity == "rare":
                if player.unlock_achievement("rare_collector"):
                    newly_unlocked.append(("rare_collector", get_achievement_by_id(achievements, "rare_collector")))
            elif item.rarity == "epic":
                if player.unlock_achievement("epic_collector"):
                    newly_unlocked.append(("epic_collector", get_achievement_by_id(achievements, "epic_collector")))
            elif item.rarity == "legendary":
                if player.unlock_achievement("legendary_collector"):
                    newly_unlocked.append(("legendary_collector", get_achievement_by_id(achievements, "legendary_collector")))

    elif trigger == "gold_changed":
        if player.gold >= 500:
            if player.unlock_achievement("gold_hoarder"):
                newly_unlocked.append(("gold_hoarder", get_achievement_by_id(achievements, "gold_hoarder")))

    elif trigger == "skill_used":
        if player.skills_used >= 50:
            if player.unlock_achievement("skill_master"):
                newly_unlocked.append(("skill_master", get_achievement_by_id(achievements, "skill_master")))

    elif trigger == "battle_won":
        hp_percent = (player.hp / player.total_max_hp) * 100
        if hp_percent < 10:
            if player.unlock_achievement("survivor"):
                newly_unlocked.append(("survivor", get_achievement_by_id(achievements, "survivor")))

        # Perfect victory (boss without damage)
        if kwargs.get("is_boss", False) and kwargs.get("damage_taken", 0) == 0:
            if player.unlock_achievement("perfect_victory"):
                newly_unlocked.append(("perfect_victory", get_achievement_by_id(achievements, "perfect_victory")))

    elif trigger == "item_purchased":
        if player.items_purchased >= 20:
            if player.unlock_achievement("shopaholic"):
                newly_unlocked.append(("shopaholic", get_achievement_by_id(achievements, "shopaholic")))

    elif trigger == "new_game_plus":
        if player.unlock_achievement("new_game_plus"):
            newly_unlocked.append(("new_game_plus", get_achievement_by_id(achievements, "new_game_plus")))

    return newly_unlocked


def format_achievement_unlock(achievement: Achievement) -> str:
    """Format an achievement unlock message."""
    name = t({"en": achievement.name_en, "zh": achievement.name_zh})
    desc = t({"en": achievement.description_en, "zh": achievement.description_zh})
    return t({"en": f"🏆 Achievement Unlocked: {name}\n   {desc}",
              "zh": f"🏆 成就解锁：{name}\n   {desc}"})
