import random
from game.floor import generate_event, load_events
from game.player import Player
from game.event import Event, EventChoice


def test_load_events():
    """Test that events can be loaded from JSON."""
    events = load_events()
    assert len(events) > 0
    assert "name" in events[0]
    assert "description" in events[0]
    assert "choices" in events[0]


def test_generate_event():
    """Test event generation."""
    rng = random.Random(42)
    event = generate_event(floor=1, rng=rng)
    # Event generation is random (50% chance), so we test both cases
    if event:
        assert isinstance(event, Event)
        assert len(event.choices) > 0
        assert event.min_floor <= 1


def test_event_heal_effect():
    """Test heal event effect."""
    player = Player(name="Test", hp=20, max_hp=50)
    result = player.apply_event_effect("heal", 15)
    assert player.hp == 35
    assert result == ""


def test_event_heal_at_full_hp():
    """Test heal event when already at full HP."""
    player = Player(name="Test", hp=50, max_hp=50)
    result = player.apply_event_effect("heal", 15)
    assert player.hp == 50
    # Should return a message indicating already at full HP
    assert len(result) > 0


def test_event_damage_effect():
    """Test damage event effect."""
    player = Player(name="Test", hp=30, max_hp=50)
    result = player.apply_event_effect("damage", 10)
    assert player.hp == 20
    assert result == ""


def test_event_gold_effect():
    """Test gold event effect."""
    player = Player(name="Test", gold=10)
    result = player.apply_event_effect("gold", 30)
    assert player.gold == 40
    assert result == ""


def test_event_gold_with_hp_cost():
    """Test gold with HP cost event effect (e.g., helping wounded adventurer)."""
    player = Player(name="Test", hp=30, max_hp=50, gold=10)
    result = player.apply_event_effect("gold_with_hp_cost", 60)
    assert player.hp == 20  # 30 - 10
    assert player.gold == 70  # 10 + 60
    assert result == ""


def test_event_trade_heal_success():
    """Test trade heal event with sufficient gold."""
    player = Player(name="Test", hp=20, max_hp=50, gold=50)
    result = player.apply_event_effect("trade_heal", 25)
    assert player.hp == 45
    assert player.gold == 30  # 50 - 20
    assert result == ""


def test_event_trade_heal_insufficient_gold():
    """Test trade heal event with insufficient gold."""
    player = Player(name="Test", hp=20, max_hp=50, gold=10)
    old_hp = player.hp
    result = player.apply_event_effect("trade_heal", 25)
    assert player.hp == old_hp  # HP should not change
    assert player.gold == 10  # Gold should not change
    assert len(result) > 0  # Should return error message


def test_event_trade_gold_for_heal_success():
    """Test trade gold for heal event with sufficient gold."""
    player = Player(name="Test", hp=20, max_hp=100, gold=100)
    result = player.apply_event_effect("trade_gold_for_heal", 40)
    assert player.hp == 60
    assert player.gold == 50  # 100 - 50
    assert result == ""


def test_event_trade_gold_for_heal_insufficient_gold():
    """Test trade gold for heal event with insufficient gold."""
    player = Player(name="Test", hp=20, max_hp=100, gold=30)
    old_hp = player.hp
    result = player.apply_event_effect("trade_gold_for_heal", 40)
    assert player.hp == old_hp  # HP should not change
    assert player.gold == 30  # Gold should not change
    assert len(result) > 0  # Should return error message


def test_event_nothing_effect():
    """Test nothing event effect."""
    player = Player(name="Test", hp=30, max_hp=50, gold=20)
    old_hp = player.hp
    old_gold = player.gold
    result = player.apply_event_effect("nothing", 0)
    assert player.hp == old_hp
    assert player.gold == old_gold
    assert result == ""


def test_event_choice_structure():
    """Test that event choices have proper structure."""
    events = load_events()
    for event_data in events:
        assert "choices" in event_data
        assert len(event_data["choices"]) >= 2
        for choice in event_data["choices"]:
            assert "text" in choice
            assert "effect_type" in choice
            assert "effect_value" in choice
            assert "result_text" in choice
