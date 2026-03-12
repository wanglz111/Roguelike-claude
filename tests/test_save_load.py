"""Tests for save and load functionality."""
import os
import tempfile
from pathlib import Path

from game.game_state import GameState
from game.player import Player
from game.item import Item
from game.save_load import save_game, load_game, SAVE_DIR, SAVE_FILE


def test_save_and_load_basic():
    """Test basic save and load functionality."""
    # Create a test game state
    player = Player(name="TestHero", hp=25, max_hp=30, attack=10, defense=5, level=2, exp=15, gold=50)
    state = GameState(player=player, floor=3, max_floor=5, game_over=False)
    state.log.append("Test log entry")

    # Save the game
    msg = save_game(state)
    assert "saved" in msg.lower() or "保存" in msg

    # Load the game
    loaded_state, msg = load_game()
    assert loaded_state is not None
    assert "loaded" in msg.lower() or "加载" in msg

    # Verify player data
    assert loaded_state.player.name == "TestHero"
    assert loaded_state.player.hp == 25
    assert loaded_state.player.max_hp == 30
    assert loaded_state.player.attack == 10
    assert loaded_state.player.defense == 5
    assert loaded_state.player.level == 2
    assert loaded_state.player.exp == 15
    assert loaded_state.player.gold == 50

    # Verify game state
    assert loaded_state.floor == 3
    assert loaded_state.max_floor == 5
    assert loaded_state.game_over is False
    assert "Test log entry" in loaded_state.log


def test_save_and_load_with_inventory():
    """Test save and load with items in inventory."""
    player = Player(name="TestHero")

    # Add items to inventory
    potion = Item(
        name={"en": "Health Potion", "zh": "生命药水"},
        item_type="consumable",
        effect_type="heal",
        effect_value=20,
        description={"en": "Restores 20 HP", "zh": "恢复20点生命值"}
    )
    player.inventory.append(potion)

    state = GameState(player=player, floor=2)

    # Save and load
    save_game(state)
    loaded_state, _ = load_game()

    # Verify inventory
    assert len(loaded_state.player.inventory) == 1
    assert loaded_state.player.inventory[0].item_type == "consumable"
    assert loaded_state.player.inventory[0].effect_type == "heal"
    assert loaded_state.player.inventory[0].effect_value == 20


def test_save_and_load_with_equipment():
    """Test save and load with equipped items."""
    player = Player(name="TestHero")

    # Create and equip weapon
    sword = Item(
        name={"en": "Iron Sword", "zh": "铁剑"},
        item_type="equipment",
        effect_type="none",
        effect_value=0,
        description={"en": "A basic sword", "zh": "基础剑"},
        equipment_slot="weapon",
        bonus_attack=5,
        bonus_defense=0,
        bonus_hp=0
    )
    player.weapon = sword

    # Create and equip armor
    armor = Item(
        name={"en": "Leather Armor", "zh": "皮甲"},
        item_type="equipment",
        effect_type="none",
        effect_value=0,
        description={"en": "Basic armor", "zh": "基础护甲"},
        equipment_slot="armor",
        bonus_attack=0,
        bonus_defense=3,
        bonus_hp=5
    )
    player.armor = armor

    state = GameState(player=player, floor=2)

    # Save and load
    save_game(state)
    loaded_state, _ = load_game()

    # Verify equipment
    assert loaded_state.player.weapon is not None
    assert loaded_state.player.weapon.equipment_slot == "weapon"
    assert loaded_state.player.weapon.bonus_attack == 5

    assert loaded_state.player.armor is not None
    assert loaded_state.player.armor.equipment_slot == "armor"
    assert loaded_state.player.armor.bonus_defense == 3
    assert loaded_state.player.armor.bonus_hp == 5

    # Verify total stats calculation works
    assert loaded_state.player.total_attack == player.attack + 5
    assert loaded_state.player.total_defense == player.defense + 3
    assert loaded_state.player.total_max_hp == player.max_hp + 5


def test_save_and_load_game_over():
    """Test save and load with game over state."""
    player = Player(name="TestHero", hp=0)
    state = GameState(player=player, floor=3, game_over=True)
    state.log.append("You have fallen...")

    # Save and load
    save_game(state)
    loaded_state, _ = load_game()

    # Verify game over state
    assert loaded_state.game_over is True
    assert loaded_state.player.hp == 0
    assert not loaded_state.player.is_alive
