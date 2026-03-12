import random
from game.floor import generate_monster
from game.monster import Monster


def test_boss_spawns_on_floor_5():
    """Test that floor 5 spawns a boss monster."""
    rng = random.Random(42)
    monster = generate_monster(5, rng)
    assert monster.is_boss is True


def test_boss_spawns_on_floor_10():
    """Test that floor 10 spawns a boss monster."""
    rng = random.Random(42)
    monster = generate_monster(10, rng)
    assert monster.is_boss is True


def test_normal_monster_on_floor_1():
    """Test that floor 1 spawns a normal monster."""
    rng = random.Random(42)
    monster = generate_monster(1, rng)
    assert monster.is_boss is False


def test_normal_monster_on_floor_4():
    """Test that floor 4 spawns a normal monster."""
    rng = random.Random(42)
    monster = generate_monster(4, rng)
    assert monster.is_boss is False


def test_normal_monster_on_floor_6():
    """Test that floor 6 spawns a normal monster."""
    rng = random.Random(42)
    monster = generate_monster(6, rng)
    assert monster.is_boss is False


def test_boss_has_higher_stats():
    """Test that boss monsters have higher stats than normal monsters."""
    rng = random.Random(42)
    normal = generate_monster(4, rng)
    boss = generate_monster(5, rng)

    # Boss should have significantly higher stats
    assert boss.hp > normal.hp
    assert boss.attack > normal.attack
    assert boss.exp_reward > normal.exp_reward
    assert boss.gold_reward > normal.gold_reward


def test_boss_scaling():
    """Test that boss stats scale with floor level."""
    rng = random.Random(42)
    boss_5 = generate_monster(5, rng)
    boss_10 = generate_monster(10, rng)

    # Floor 10 boss should be stronger than floor 5 boss
    assert boss_10.hp >= boss_5.hp
    assert boss_10.attack >= boss_5.attack


def test_monster_dataclass_has_is_boss_field():
    """Test that Monster dataclass has is_boss field with default False."""
    monster = Monster(
        name="Test Monster",
        hp=10,
        attack=5,
        defense=2,
        exp_reward=10,
        gold_reward=5
    )
    assert hasattr(monster, 'is_boss')
    assert monster.is_boss is False


def test_monster_can_be_created_as_boss():
    """Test that Monster can be explicitly created as a boss."""
    boss = Monster(
        name="Test Boss",
        hp=50,
        attack=20,
        defense=10,
        exp_reward=100,
        gold_reward=50,
        is_boss=True
    )
    assert boss.is_boss is True
