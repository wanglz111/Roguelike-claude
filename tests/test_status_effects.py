import pytest
from game.player import Player
from game.status_effect import load_status_effects, ActiveStatusEffect


def test_load_status_effects():
    """Test that status effects load correctly from JSON."""
    effects = load_status_effects()
    assert len(effects) >= 6  # At least 6 status effects defined
    assert "poison" in effects
    assert "burn" in effects
    assert "freeze" in effects
    assert "bleed" in effects
    assert "regen" in effects
    assert "weaken" in effects


def test_poison_effect():
    """Test poison status effect deals damage over time."""
    player = Player(name="Test Hero")
    effects = load_status_effects()
    poison = effects["poison"]

    # Apply poison
    active_poison = ActiveStatusEffect(effect=poison, remaining_turns=poison.duration)
    player.add_status_effect(active_poison)

    assert len(player.status_effects) == 1
    initial_hp = player.hp

    # Process one turn
    messages = player.process_status_effects()
    assert player.hp < initial_hp  # Should take damage
    assert len(messages) > 0  # Should have damage message


def test_regen_effect():
    """Test regeneration status effect heals over time."""
    player = Player(name="Test Hero")
    player.hp = 20  # Reduce HP
    effects = load_status_effects()
    regen = effects["regen"]

    # Apply regen
    active_regen = ActiveStatusEffect(effect=regen, remaining_turns=regen.duration)
    player.add_status_effect(active_regen)

    initial_hp = player.hp

    # Process one turn
    messages = player.process_status_effects()
    assert player.hp > initial_hp  # Should heal
    assert len(messages) > 0  # Should have heal message


def test_freeze_effect_reduces_attack():
    """Test freeze status effect reduces attack."""
    player = Player(name="Test Hero")
    effects = load_status_effects()
    freeze = effects["freeze"]

    initial_attack = player.total_attack

    # Apply freeze
    active_freeze = ActiveStatusEffect(effect=freeze, remaining_turns=freeze.duration)
    player.add_status_effect(active_freeze)

    # Attack should be reduced
    assert player.total_attack < initial_attack
    assert player.total_attack == int(initial_attack * freeze.attack_modifier)


def test_weaken_effect_reduces_attack_and_defense():
    """Test weaken status effect reduces both attack and defense."""
    player = Player(name="Test Hero")
    effects = load_status_effects()
    weaken = effects["weaken"]

    initial_attack = player.total_attack
    initial_defense = player.total_defense

    # Apply weaken
    active_weaken = ActiveStatusEffect(effect=weaken, remaining_turns=weaken.duration)
    player.add_status_effect(active_weaken)

    # Both attack and defense should be reduced
    assert player.total_attack < initial_attack
    assert player.total_defense < initial_defense


def test_status_effect_expires():
    """Test that status effects expire after their duration."""
    player = Player(name="Test Hero")
    effects = load_status_effects()
    poison = effects["poison"]

    # Apply poison with 2 turns duration
    active_poison = ActiveStatusEffect(effect=poison, remaining_turns=2)
    player.add_status_effect(active_poison)

    assert len(player.status_effects) == 1

    # Process first turn
    player.process_status_effects()
    assert len(player.status_effects) == 1  # Still active

    # Process second turn
    messages = player.process_status_effects()
    assert len(player.status_effects) == 0  # Should be expired
    # Check for expiration message
    assert any("worn off" in msg or "消失" in msg for msg in messages)


def test_status_effect_refresh():
    """Test that applying the same effect refreshes duration instead of stacking."""
    player = Player(name="Test Hero")
    effects = load_status_effects()
    poison = effects["poison"]

    # Apply poison
    active_poison1 = ActiveStatusEffect(effect=poison, remaining_turns=1)
    player.add_status_effect(active_poison1)

    assert len(player.status_effects) == 1
    assert player.status_effects[0].remaining_turns == 1

    # Apply poison again
    active_poison2 = ActiveStatusEffect(effect=poison, remaining_turns=3)
    player.add_status_effect(active_poison2)

    # Should still have only 1 effect, but with refreshed duration
    assert len(player.status_effects) == 1
    assert player.status_effects[0].remaining_turns == 3


def test_multiple_status_effects():
    """Test that multiple different status effects can be active simultaneously."""
    player = Player(name="Test Hero")
    effects = load_status_effects()

    # Apply poison and freeze
    poison = ActiveStatusEffect(effect=effects["poison"], remaining_turns=3)
    freeze = ActiveStatusEffect(effect=effects["freeze"], remaining_turns=2)

    player.add_status_effect(poison)
    player.add_status_effect(freeze)

    assert len(player.status_effects) == 2


def test_clear_status_effects():
    """Test that clear_status_effects removes all effects."""
    player = Player(name="Test Hero")
    effects = load_status_effects()

    # Apply multiple effects
    player.add_status_effect(ActiveStatusEffect(effect=effects["poison"], remaining_turns=3))
    player.add_status_effect(ActiveStatusEffect(effect=effects["freeze"], remaining_turns=2))

    assert len(player.status_effects) == 2

    # Clear all effects
    player.clear_status_effects()

    assert len(player.status_effects) == 0


def test_burn_effect():
    """Test burn status effect deals damage over time."""
    player = Player(name="Test Hero")
    effects = load_status_effects()
    burn = effects["burn"]

    initial_hp = player.hp

    # Apply burn
    active_burn = ActiveStatusEffect(effect=burn, remaining_turns=burn.duration)
    player.add_status_effect(active_burn)

    # Process one turn
    player.process_status_effects()

    # Should take damage (burn deals 5 damage per turn)
    assert player.hp == initial_hp - burn.damage_per_turn


def test_bleed_effect():
    """Test bleed status effect deals damage over time."""
    player = Player(name="Test Hero")
    effects = load_status_effects()
    bleed = effects["bleed"]

    initial_hp = player.hp

    # Apply bleed
    active_bleed = ActiveStatusEffect(effect=bleed, remaining_turns=bleed.duration)
    player.add_status_effect(active_bleed)

    # Process one turn
    player.process_status_effects()

    # Should take damage (bleed deals 4 damage per turn)
    assert player.hp == initial_hp - bleed.damage_per_turn
