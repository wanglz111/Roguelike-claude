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

    def test_lich_king_boss(self):
        """Test floor 10 boss (Lich King) encounter."""
        rng = random.Random(42)
        player = Player(name="Test", hp=80, max_hp=80, attack=24, defense=10, level=8, exp=0)

        boss = generate_monster(10, rng)
        self.assertTrue(boss.is_boss, "Floor 10 should spawn Lich King boss")
        self.assertEqual(boss.name, "Lich King")

        won, _ = fight(player, boss)
        self.assertTrue(won, "Player should defeat Lich King with level 8 stats")
        self.assertLess(player.hp, player.total_max_hp * 0.6, "Lich King should deal significant damage")

    def test_ancient_dragon_boss(self):
        """Test floor 15 boss (Ancient Dragon) encounter."""
        rng = random.Random(42)
        player = Player(name="Test", hp=110, max_hp=110, attack=34, defense=15, level=12, exp=0)

        boss = generate_monster(15, rng)
        self.assertTrue(boss.is_boss, "Floor 15 should spawn Ancient Dragon boss")
        self.assertEqual(boss.name, "Ancient Dragon")

        won, _ = fight(player, boss)
        self.assertTrue(won, "Player should defeat Ancient Dragon with level 12 stats")
        self.assertLess(player.hp, player.total_max_hp * 0.5, "Ancient Dragon should deal heavy damage")

    def test_demon_lord_boss(self):
        """Test floor 20 boss (Demon Lord) encounter."""
        rng = random.Random(42)
        player = Player(name="Test", hp=140, max_hp=140, attack=44, defense=20, level=16, exp=0)

        boss = generate_monster(20, rng)
        self.assertTrue(boss.is_boss, "Floor 20 should spawn Demon Lord boss")
        self.assertEqual(boss.name, "Demon Lord")

        won, _ = fight(player, boss)
        self.assertTrue(won, "Player should defeat Demon Lord with level 16 stats")
        self.assertLess(player.hp, player.total_max_hp * 0.4, "Demon Lord should deal massive damage")


if __name__ == "__main__":
    unittest.main()
