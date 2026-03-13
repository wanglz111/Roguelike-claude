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

        # Monster Hunter
        if player.monsters_killed >= 50:
            if player.unlock_achievement("monster_hunter"):
                newly_unlocked.append(("monster_hunter", get_achievement_by_id(achievements, "monster_hunter")))

        # Boss achievements
        if kwargs.get("is_boss", False):
            if player.bosses_killed == 1:
                if player.unlock_achievement("boss_slayer"):
                    newly_unlocked.append(("boss_slayer", get_achievement_by_id(achievements, "boss_slayer")))

            # Boss Master (all 4 bosses defeated)
            if player.bosses_killed == 4:
                if player.unlock_achievement("boss_master"):
                    newly_unlocked.append(("boss_master", get_achievement_by_id(achievements, "boss_master")))

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

        # Speed Runner (reach floor 10 before level 8)
        if floor == 10 and player.level < 8:
            if player.unlock_achievement("speed_runner"):
                newly_unlocked.append(("speed_runner", get_achievement_by_id(achievements, "speed_runner")))

        # Completion achievement
        if floor > 20:
            if player.unlock_achievement("first_completion"):
                newly_unlocked.append(("first_completion", get_achievement_by_id(achievements, "first_completion")))

            # Track completed class
            player.completed_classes.add(player.player_class)

            # Class-specific completion achievements
            if player.player_class == "warrior":
                if player.unlock_achievement("warrior_champion"):
                    newly_unlocked.append(("warrior_champion", get_achievement_by_id(achievements, "warrior_champion")))
            elif player.player_class == "mage":
                if player.unlock_achievement("mage_champion"):
                    newly_unlocked.append(("mage_champion", get_achievement_by_id(achievements, "mage_champion")))

            # Versatile Hero (complete with 3 different classes)
            if len(player.completed_classes) >= 3:
                if player.unlock_achievement("versatile_hero"):
                    newly_unlocked.append(("versatile_hero", get_achievement_by_id(achievements, "versatile_hero")))

            # Difficulty-based completion achievements
            difficulty = kwargs.get("difficulty", None)
            if difficulty:
                from game.difficulty import Difficulty
                if difficulty == Difficulty.EASY:
                    if player.unlock_achievement("easy_completion"):
                        newly_unlocked.append(("easy_completion", get_achievement_by_id(achievements, "easy_completion")))
                elif difficulty == Difficulty.HARD:
                    if player.unlock_achievement("hard_completion"):
                        newly_unlocked.append(("hard_completion", get_achievement_by_id(achievements, "hard_completion")))

            # Cycle Veteran (complete cycle 3 or higher)
            cycle = kwargs.get("cycle", 1)
            if cycle >= 3:
                if player.unlock_achievement("cycle_veteran"):
                    newly_unlocked.append(("cycle_veteran", get_achievement_by_id(achievements, "cycle_veteran")))

        # Hard difficulty floor 10 achievement
        if floor == 10:
            difficulty = kwargs.get("difficulty", None)
            if difficulty:
                from game.difficulty import Difficulty
                if difficulty == Difficulty.HARD:
                    if player.unlock_achievement("hard_survivor"):
                        newly_unlocked.append(("hard_survivor", get_achievement_by_id(achievements, "hard_survivor")))

    elif trigger == "level_up":
        level = player.level
        if level == 10:
            if player.unlock_achievement("level_10"):
                newly_unlocked.append(("level_10", get_achievement_by_id(achievements, "level_10")))
        elif level == 15:
            if player.unlock_achievement("class_master"):
                newly_unlocked.append(("class_master", get_achievement_by_id(achievements, "class_master")))
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

        # Set Collector - check if wearing a complete set
        active_set = player.get_active_set_bonus()
        if active_set:
            if player.unlock_achievement("set_collector"):
                newly_unlocked.append(("set_collector", get_achievement_by_id(achievements, "set_collector")))

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
        if player.gold >= 1000:
            if player.unlock_achievement("wealthy_adventurer"):
                newly_unlocked.append(("wealthy_adventurer", get_achievement_by_id(achievements, "wealthy_adventurer")))

    elif trigger == "skill_used":
        if player.skills_used >= 50:
            if player.unlock_achievement("skill_master"):
                newly_unlocked.append(("skill_master", get_achievement_by_id(achievements, "skill_master")))
        if player.skills_used >= 100:
            if player.unlock_achievement("skill_specialist"):
                newly_unlocked.append(("skill_specialist", get_achievement_by_id(achievements, "skill_specialist")))

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
