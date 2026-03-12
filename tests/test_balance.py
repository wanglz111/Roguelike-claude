import unittest
import random
from game.player import Player
from game.combat import fight
from game.floor import generate_monster


class BalanceTests(unittest.TestCase):
    def test_player_can_survive_early_floors(self):
        """Test that a player can survive floors 1-5 without equipment."""
        rng = random.Random(42)
        player = Player(name="Test", hp=30, max_hp=30, attack=8, defense=3, level=1, exp=0)

        for floor in range(1, 6):
            monster = generate_monster(floor, rng)
            won, _ = fight(player, monster)
            self.assertTrue(won, f"Player died on floor {floor}")

            if player.hp < player.total_max_hp * 0.3:
                player.hp = player.total_max_hp

    def test_boss_floors_are_challenging(self):
        """Test that boss encounters require proper preparation."""
        rng = random.Random(42)
        player = Player(name="Test", hp=50, max_hp=50, attack=15, defense=6, level=5, exp=0)

        boss = generate_monster(5, rng)
        self.assertTrue(boss.is_boss, "Floor 5 should spawn a boss")

        won, _ = fight(player, boss)
        self.assertTrue(won, "Player should be able to defeat floor 5 boss with proper stats")
        self.assertLess(player.hp, player.total_max_hp * 0.5, "Boss should deal significant damage")

    def test_progression_scaling(self):
        """Test that player stats scale appropriately with level."""
        player = Player(name="Test", hp=30, max_hp=30, attack=8, defense=3, level=1, exp=0)

        initial_attack = player.attack
        initial_defense = player.defense
        initial_max_hp = player.max_hp

        player.gain_rewards(exp=100, gold=0)

        self.assertGreater(player.level, 1)
        self.assertEqual(player.attack, initial_attack + (player.level - 1) * 2)
        self.assertEqual(player.defense, initial_defense + (player.level - 1) * 1)
        self.assertEqual(player.max_hp, initial_max_hp + (player.level - 1) * 6)


if __name__ == "__main__":
    unittest.main()
