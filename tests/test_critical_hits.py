import random
from game.combat import calculate_damage, check_critical_hit, fight
from game.player import Player
from game.monster import Monster


def test_calculate_damage_normal():
    """Test normal damage calculation."""
    damage = calculate_damage(attack=10, defense=3, is_critical=False)
    assert damage == 7


def test_calculate_damage_critical():
    """Test critical damage calculation (2x multiplier)."""
    damage = calculate_damage(attack=10, defense=3, is_critical=True)
    assert damage == 14


def test_calculate_damage_minimum():
    """Test that damage has a minimum of 1."""
    damage = calculate_damage(attack=5, defense=10, is_critical=False)
    assert damage == 1


def test_calculate_damage_critical_minimum():
    """Test that critical damage also respects minimum (1 * 2 = 2)."""
    damage = calculate_damage(attack=5, defense=10, is_critical=True)
    assert damage == 2


def test_check_critical_hit_probability():
    """Test that critical hits occur at approximately the expected rate."""
    random.seed(42)
    trials = 1000
    crits = sum(1 for _ in range(trials) if check_critical_hit(0.1))
    # With 10% chance, expect around 100 crits in 1000 trials
    # Allow for some variance (70-130 is reasonable)
    assert 70 <= crits <= 130


def test_fight_with_critical_hits():
    """Test that fight can complete with critical hit system."""
    random.seed(42)
    player = Player(name="Hero", hp=50, max_hp=50, attack=15, defense=5)
    monster = Monster(
        name={"en": "Goblin", "zh": "哥布林"},
        hp=20,
        attack=8,
        defense=2,
        exp_reward=10,
        gold_reward=5
    )

    victory, log = fight(player, monster)

    # Player should win with these stats
    assert victory is True
    assert player.is_alive
    assert monster.hp <= 0
    assert len(log) > 0

    # Check that combat log contains messages
    log_text = " ".join(log)
    assert "Goblin" in log_text or "哥布林" in log_text


def test_critical_hit_appears_in_log():
    """Test that critical hits are mentioned in combat log."""
    random.seed(123)  # Seed that should produce at least one crit
    player = Player(name="Hero", hp=100, max_hp=100, attack=20, defense=5)
    monster = Monster(
        name={"en": "Orc", "zh": "兽人"},
        hp=30,
        attack=10,
        defense=3,
        exp_reward=15,
        gold_reward=8
    )

    victory, log = fight(player, monster)

    # Run multiple times to increase chance of seeing a crit
    found_crit = False
    for _ in range(10):
        random.seed(random.randint(0, 1000))
        player = Player(name="Hero", hp=100, max_hp=100, attack=20, defense=5)
        monster = Monster(
            name={"en": "Orc", "zh": "兽人"},
            hp=30,
            attack=10,
            defense=3,
            exp_reward=15,
            gold_reward=8
        )
        victory, log = fight(player, monster)
        log_text = " ".join(log)
        if "Critical" in log_text or "暴击" in log_text:
            found_crit = True
            break

    # With 10 fights, very likely to see at least one crit
    assert found_crit
