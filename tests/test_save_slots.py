"""Test save slot functionality."""
import os
import tempfile
from pathlib import Path
from unittest.mock import patch

from game.game_state import GameState
from game.player import Player
from game.save_load import save_game, load_game, list_save_slots, get_save_path, has_save_file, has_any_save


def test_save_and_load_multiple_slots():
    """Test saving and loading from different slots."""
    with tempfile.TemporaryDirectory() as tmpdir:
        with patch('game.save_load.SAVE_DIR', Path(tmpdir)):
            # Create three different players
            player1 = Player(name="Hero1", max_hp=100, hp=100, attack=10, defense=5)
            player2 = Player(name="Hero2", max_hp=150, hp=150, attack=15, defense=8)
            player3 = Player(name="Hero3", max_hp=200, hp=200, attack=20, defense=10)

            state1 = GameState(player=player1, floor=5)
            state2 = GameState(player=player2, floor=10)
            state3 = GameState(player=player3, floor=15)

            # Save to different slots
            save_game(state1, slot=1)
            save_game(state2, slot=2)
            save_game(state3, slot=3)

            # Verify all slots exist
            assert has_save_file(1)
            assert has_save_file(2)
            assert has_save_file(3)
            assert has_any_save()

            # Load from each slot and verify
            loaded1, _ = load_game(slot=1)
            assert loaded1.player.name == "Hero1"
            assert loaded1.floor == 5

            loaded2, _ = load_game(slot=2)
            assert loaded2.player.name == "Hero2"
            assert loaded2.floor == 10

            loaded3, _ = load_game(slot=3)
            assert loaded3.player.name == "Hero3"
            assert loaded3.floor == 15


def test_list_save_slots():
    """Test listing save slots."""
    with tempfile.TemporaryDirectory() as tmpdir:
        with patch('game.save_load.SAVE_DIR', Path(tmpdir)):
            # Initially all slots should be empty
            slots = list_save_slots()
            assert len(slots) == 3
            assert all(not exists for _, exists, _ in slots)

            # Save to slot 1
            player = Player(name="TestHero", max_hp=100, hp=100, attack=10, defense=5, level=5)
            state = GameState(player=player, floor=7, cycle=2)
            save_game(state, slot=1)

            # Check slot list
            slots = list_save_slots()
            assert slots[0][1] == True  # Slot 1 exists
            assert slots[0][2]["name"] == "TestHero"
            assert slots[0][2]["level"] == 5
            assert slots[0][2]["floor"] == 7
            assert slots[0][2]["cycle"] == 2
            assert slots[1][1] == False  # Slot 2 empty
            assert slots[2][1] == False  # Slot 3 empty


def test_overwrite_slot():
    """Test overwriting an existing slot."""
    with tempfile.TemporaryDirectory() as tmpdir:
        with patch('game.save_load.SAVE_DIR', Path(tmpdir)):
            # Save first state
            player1 = Player(name="First", max_hp=100, hp=100, attack=10, defense=5)
            state1 = GameState(player=player1, floor=5)
            save_game(state1, slot=1)

            # Overwrite with second state
            player2 = Player(name="Second", max_hp=200, hp=200, attack=20, defense=10)
            state2 = GameState(player=player2, floor=10)
            save_game(state2, slot=1)

            # Load and verify it's the second state
            loaded, _ = load_game(slot=1)
            assert loaded.player.name == "Second"
            assert loaded.floor == 10
