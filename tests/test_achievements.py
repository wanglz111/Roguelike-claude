"""Tests for achievement system."""

import pytest
from game.achievement import load_achievements, get_achievement_by_id
from game.achievement_checker import check_achievements
from game.player import Player
from game.item import Item


def test_load_achievements():
    """Test loading achievements from JSON."""
    achievements = load_achievements()
    assert len(achievements) == 38  # Total number of achievements (33 + 5 new)

    # Check that all achievements have required fields
    for ach in achievements:
        assert ach.id
        assert ach.name_en
        assert ach.name_zh
        assert ach.description_en
        assert ach.description_zh
        assert ach.category in ["combat", "exploration", "progression", "collection"]


def test_get_achievement_by_id():
    """Test getting achievement by ID."""
    achievements = load_achievements()

    ach = get_achievement_by_id(achievements, "first_blood")
    assert ach is not None
    assert ach.id == "first_blood"

    ach = get_achievement_by_id(achievements, "nonexistent")
    assert ach is None


def test_first_blood_achievement():
    """Test first blood achievement (kill first monster)."""
    achievements = load_achievements()
    player = Player(name="Test Hero")

    # No achievement before first kill
    assert "first_blood" not in player.unlocked_achievements

    # Kill first monster
    player.monsters_killed = 1
    newly_unlocked = check_achievements(player, achievements, "monster_killed", is_boss=False)

    assert len(newly_unlocked) == 1
    assert newly_unlocked[0][0] == "first_blood"
    assert "first_blood" in player.unlocked_achievements


def test_boss_slayer_achievement():
    """Test boss slayer achievement (kill first boss)."""
    achievements = load_achievements()
    player = Player(name="Test Hero")

    # Kill first boss
    player.monsters_killed = 1
    player.bosses_killed = 1
    newly_unlocked = check_achievements(player, achievements, "monster_killed", is_boss=True, monster_name="Goblin Warlord")

    # Should unlock both boss_slayer and goblin_warlord_defeated
    assert len(newly_unlocked) == 2
    achievement_ids = [ach_id for ach_id, _ in newly_unlocked]
    assert "boss_slayer" in achievement_ids
    assert "goblin_warlord_defeated" in achievement_ids


def test_floor_achievements():
    """Test floor milestone achievements."""
    achievements = load_achievements()
    player = Player(name="Test Hero")

    # Reach floor 5
    newly_unlocked = check_achievements(player, achievements, "floor_reached", floor=5)
    assert len(newly_unlocked) == 1
    assert newly_unlocked[0][0] == "floor_5"

    # Reach floor 10
    newly_unlocked = check_achievements(player, achievements, "floor_reached", floor=10)
    assert len(newly_unlocked) == 1
    assert newly_unlocked[0][0] == "floor_10"


def test_level_achievements():
    """Test level milestone achievements."""
    achievements = load_achievements()
    player = Player(name="Test Hero")

    # Reach level 10
    player.level = 10
    newly_unlocked = check_achievements(player, achievements, "level_up")
    assert len(newly_unlocked) == 1
    assert newly_unlocked[0][0] == "level_10"

    # Reach level 20
    player.level = 20
    newly_unlocked = check_achievements(player, achievements, "level_up")
    assert len(newly_unlocked) == 1
    assert newly_unlocked[0][0] == "level_20"


def test_equipment_achievements():
    """Test equipment-related achievements."""
    achievements = load_achievements()
    player = Player(name="Test Hero")

    # Equip first item
    weapon = Item(name="Sword", item_type="equipment", equipment_slot="weapon", bonus_attack=5)
    player.weapon = weapon
    newly_unlocked = check_achievements(player, achievements, "equipment_equipped", item=weapon)
    assert "first_equipment" in [ach_id for ach_id, _ in newly_unlocked]

    # Equip full set
    armor = Item(name="Armor", item_type="equipment", equipment_slot="armor", bonus_defense=3)
    accessory = Item(name="Ring", item_type="equipment", equipment_slot="accessory", bonus_hp=10)
    player.armor = armor
    player.accessory = accessory
    newly_unlocked = check_achievements(player, achievements, "equipment_equipped", item=accessory)
    assert "full_equipment" in [ach_id for ach_id, _ in newly_unlocked]


def test_rarity_achievements():
    """Test equipment rarity achievements."""
    achievements = load_achievements()
    player = Player(name="Test Hero")

    # Equip rare item
    rare_weapon = Item(name="Rare Sword", item_type="equipment", equipment_slot="weapon",
                       bonus_attack=5, rarity="rare")
    player.weapon = rare_weapon
    newly_unlocked = check_achievements(player, achievements, "equipment_equipped", item=rare_weapon)
    assert "rare_collector" in [ach_id for ach_id, _ in newly_unlocked]

    # Equip epic item
    epic_weapon = Item(name="Epic Sword", item_type="equipment", equipment_slot="weapon",
                       bonus_attack=8, rarity="epic")
    player.weapon = epic_weapon
    newly_unlocked = check_achievements(player, achievements, "equipment_equipped", item=epic_weapon)
    assert "epic_collector" in [ach_id for ach_id, _ in newly_unlocked]


def test_gold_hoarder_achievement():
    """Test gold accumulation achievement."""
    achievements = load_achievements()
    player = Player(name="Test Hero")

    # Accumulate 500 gold
    player.gold = 500
    newly_unlocked = check_achievements(player, achievements, "gold_changed")
    assert len(newly_unlocked) == 1
    assert newly_unlocked[0][0] == "gold_hoarder"


def test_skill_master_achievement():
    """Test skill usage achievement."""
    achievements = load_achievements()
    player = Player(name="Test Hero")

    # Use 50 skills
    player.skills_used = 50
    newly_unlocked = check_achievements(player, achievements, "skill_used")
    assert len(newly_unlocked) == 1
    assert newly_unlocked[0][0] == "skill_master"


def test_survivor_achievement():
    """Test survivor achievement (win with <10% HP)."""
    achievements = load_achievements()
    player = Player(name="Test Hero", max_hp=100, hp=5)

    newly_unlocked = check_achievements(player, achievements, "battle_won", is_boss=False, damage_taken=0)
    assert len(newly_unlocked) == 1
    assert newly_unlocked[0][0] == "survivor"


def test_perfect_victory_achievement():
    """Test perfect victory achievement (beat boss without damage)."""
    achievements = load_achievements()
    player = Player(name="Test Hero")

    newly_unlocked = check_achievements(player, achievements, "battle_won", is_boss=True, damage_taken=0)
    assert len(newly_unlocked) == 1
    assert newly_unlocked[0][0] == "perfect_victory"


def test_shopaholic_achievement():
    """Test shopaholic achievement (purchase 20 items)."""
    achievements = load_achievements()
    player = Player(name="Test Hero")

    # Purchase 20 items
    player.items_purchased = 20
    newly_unlocked = check_achievements(player, achievements, "item_purchased")
    assert len(newly_unlocked) == 1
    assert newly_unlocked[0][0] == "shopaholic"


def test_new_game_plus_achievement():
    """Test New Game+ achievement."""
    achievements = load_achievements()
    player = Player(name="Test Hero")

    newly_unlocked = check_achievements(player, achievements, "new_game_plus")
    assert len(newly_unlocked) == 1
    assert newly_unlocked[0][0] == "new_game_plus"


def test_achievement_not_unlocked_twice():
    """Test that achievements are not unlocked twice."""
    achievements = load_achievements()
    player = Player(name="Test Hero")

    # First unlock
    player.monsters_killed = 1
    newly_unlocked = check_achievements(player, achievements, "monster_killed", is_boss=False)
    assert len(newly_unlocked) == 1

    # Second check should not unlock again
    newly_unlocked = check_achievements(player, achievements, "monster_killed", is_boss=False)
    assert len(newly_unlocked) == 0


def test_player_achievement_methods():
    """Test Player achievement tracking methods."""
    player = Player(name="Test Hero")

    # Initially no achievements
    assert len(player.unlocked_achievements) == 0
    assert not player.has_achievement("first_blood")

    # Unlock achievement
    result = player.unlock_achievement("first_blood")
    assert result is True
    assert player.has_achievement("first_blood")
    assert len(player.unlocked_achievements) == 1

    # Try to unlock again
    result = player.unlock_achievement("first_blood")
    assert result is False
    assert len(player.unlocked_achievements) == 1


def test_monster_hunter_achievement():
    """Test monster hunter achievement (50 kills)."""
    achievements = load_achievements()
    player = Player(name="Test Hero")

    # 49 kills - no achievement
    player.monsters_killed = 49
    newly_unlocked = check_achievements(player, achievements, "monster_killed", is_boss=False)
    assert len(newly_unlocked) == 0

    # 50 kills - achievement unlocked
    player.monsters_killed = 50
    newly_unlocked = check_achievements(player, achievements, "monster_killed", is_boss=False)
    assert len(newly_unlocked) == 1
    assert newly_unlocked[0][0] == "monster_hunter"


def test_boss_master_achievement():
    """Test boss master achievement (defeat all 4 bosses)."""
    achievements = load_achievements()
    player = Player(name="Test Hero")

    # 3 bosses - no achievement
    player.bosses_killed = 3
    newly_unlocked = check_achievements(player, achievements, "monster_killed", is_boss=True, monster_name="Ancient Dragon")
    assert "boss_master" not in [ach_id for ach_id, _ in newly_unlocked]

    # 4 bosses - achievement unlocked
    player.bosses_killed = 4
    newly_unlocked = check_achievements(player, achievements, "monster_killed", is_boss=True, monster_name="Demon Lord")
    assert any(ach_id == "boss_master" for ach_id, _ in newly_unlocked)


def test_speed_runner_achievement():
    """Test speed runner achievement (reach floor 10 before level 8)."""
    achievements = load_achievements()
    player = Player(name="Test Hero")

    # Level 8 at floor 10 - no achievement
    player.level = 8
    newly_unlocked = check_achievements(player, achievements, "floor_reached", floor=10, cycle=1)
    assert "speed_runner" not in [ach_id for ach_id, _ in newly_unlocked]

    # Level 7 at floor 10 - achievement unlocked
    player = Player(name="Test Hero")
    player.level = 7
    newly_unlocked = check_achievements(player, achievements, "floor_reached", floor=10, cycle=1)
    assert any(ach_id == "speed_runner" for ach_id, _ in newly_unlocked)


def test_wealthy_adventurer_achievement():
    """Test wealthy adventurer achievement (1000 gold)."""
    achievements = load_achievements()
    player = Player(name="Test Hero")

    # 999 gold - no achievement
    player.gold = 999
    newly_unlocked = check_achievements(player, achievements, "gold_changed")
    assert "wealthy_adventurer" not in [ach_id for ach_id, _ in newly_unlocked]

    # 1000 gold - achievement unlocked
    player.gold = 1000
    newly_unlocked = check_achievements(player, achievements, "gold_changed")
    assert any(ach_id == "wealthy_adventurer" for ach_id, _ in newly_unlocked)


def test_skill_specialist_achievement():
    """Test skill specialist achievement (100 skills used)."""
    achievements = load_achievements()
    player = Player(name="Test Hero")

    # 99 skills - no achievement
    player.skills_used = 99
    newly_unlocked = check_achievements(player, achievements, "skill_used")
    assert "skill_specialist" not in [ach_id for ach_id, _ in newly_unlocked]

    # 100 skills - achievement unlocked
    player.skills_used = 100
    newly_unlocked = check_achievements(player, achievements, "skill_used")
    assert any(ach_id == "skill_specialist" for ach_id, _ in newly_unlocked)


def test_cycle_veteran_achievement():
    """Test cycle veteran achievement (complete cycle 3+)."""
    achievements = load_achievements()
    player = Player(name="Test Hero")

    # Cycle 2 completion - no achievement
    newly_unlocked = check_achievements(player, achievements, "floor_reached", floor=21, cycle=2)
    assert "cycle_veteran" not in [ach_id for ach_id, _ in newly_unlocked]

    # Cycle 3 completion - achievement unlocked
    newly_unlocked = check_achievements(player, achievements, "floor_reached", floor=21, cycle=3)
    assert any(ach_id == "cycle_veteran" for ach_id, _ in newly_unlocked)

