"""
Comprehensive balance test - simulates full 1-20 floor playthrough
"""
import random
from game.player import Player
from game.floor import generate_monster, load_monsters
from game.combat import fight
from game.item import load_items
from game.player_class import load_classes

def test_warrior_full_run():
    """Test warrior class full playthrough with strategic item usage"""
    random.seed(100)

    monsters = load_monsters()
    items = load_items()
    classes = load_classes()
    warrior_class = classes[0]  # Warrior

    # Create warrior with class stats
    player = Player(name="Test Warrior")
    player.max_hp = warrior_class.base_hp
    player.hp = warrior_class.base_hp
    player.max_mp = warrior_class.base_mp
    player.mp = warrior_class.base_mp
    player.attack = warrior_class.base_attack
    player.defense = warrior_class.base_defense
    player.hp_per_level = warrior_class.hp_per_level
    player.mp_per_level = warrior_class.mp_per_level
    player.attack_per_level = warrior_class.attack_per_level
    player.defense_per_level = warrior_class.defense_per_level
    player.player_class = warrior_class.id

    health_potion = next(i for i in items if i.name == "Health Potion")

    floors_cleared = 0
    potions_used = 0

    for floor in range(1, 21):
        monster = generate_monster(floor, monsters, random.Random(floor + 100))

        # Use health potion if HP below 40%
        if player.hp < player.total_max_hp * 0.4 and len(player.inventory) > 0:
            player.use_item(0)
            potions_used += 1

        # Fight monster
        survived, log = fight(player, monster)

        if not survived:
            break

        # Collect rewards
        player.gain_rewards(monster.exp_reward, monster.gold_reward)

        # Add health potion to inventory after each fight
        player.add_item(health_potion)

        floors_cleared += 1

    # Warrior should be able to clear at least 15 floors
    assert floors_cleared >= 15, f"Warrior only cleared {floors_cleared} floors"
    assert player.level >= 8, f"Warrior only reached level {player.level}"


def test_mage_full_run():
    """Test mage class full playthrough"""
    random.seed(200)

    monsters = load_monsters()
    items = load_items()
    classes = load_classes()
    mage_class = classes[1]  # Mage

    player = Player(name="Test Mage")
    player.max_hp = mage_class.base_hp
    player.hp = mage_class.base_hp
    player.max_mp = mage_class.base_mp
    player.mp = mage_class.base_mp
    player.attack = mage_class.base_attack
    player.defense = mage_class.base_defense
    player.hp_per_level = mage_class.hp_per_level
    player.mp_per_level = mage_class.mp_per_level
    player.attack_per_level = mage_class.attack_per_level
    player.defense_per_level = mage_class.defense_per_level
    player.player_class = mage_class.id

    health_potion = next(i for i in items if i.name == "Health Potion")

    floors_cleared = 0

    for floor in range(1, 21):
        monster = generate_monster(floor, monsters, random.Random(floor + 300))

        if player.hp < player.total_max_hp * 0.5 and len(player.inventory) > 0:
            player.use_item(0)

        survived, log = fight(player, monster)

        if not survived:
            break

        player.gain_rewards(monster.exp_reward, monster.gold_reward)
        player.add_item(health_potion)

        floors_cleared += 1

    # Mage should clear at least 12 floors (lower HP makes it harder)
    assert floors_cleared >= 12, f"Mage only cleared {floors_cleared} floors"


def test_boss_difficulty_progression():
    """Test that boss difficulty scales appropriately"""
    random.seed(300)

    monsters = load_monsters()
    classes = load_classes()
    warrior_class = classes[0]

    player = Player(name="Test Hero")
    player.max_hp = warrior_class.base_hp
    player.hp = warrior_class.base_hp
    player.max_mp = warrior_class.base_mp
    player.mp = warrior_class.base_mp
    player.attack = warrior_class.base_attack
    player.defense = warrior_class.base_defense
    player.hp_per_level = warrior_class.hp_per_level
    player.mp_per_level = warrior_class.mp_per_level
    player.attack_per_level = warrior_class.attack_per_level
    player.defense_per_level = warrior_class.defense_per_level

    boss_floors = [5, 10, 15, 20]

    for boss_floor in boss_floors:
        # Level up player to appropriate level for boss
        target_level = boss_floor // 2
        while player.level < target_level:
            player.gain_rewards(100, 0)

        player.hp = player.total_max_hp  # Full heal before boss

        boss = generate_monster(boss_floor, monsters, random.Random(boss_floor + 500))

        assert boss.is_boss, f"Floor {boss_floor} should spawn a boss"

        initial_hp = player.hp
        survived, log = fight(player, boss)

        # Boss should deal significant damage (at least 30% of max HP)
        damage_taken = initial_hp - player.hp
        assert damage_taken >= player.total_max_hp * 0.3, \
            f"Boss at floor {boss_floor} only dealt {damage_taken} damage"
