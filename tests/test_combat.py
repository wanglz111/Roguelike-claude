import unittest

from game.combat import calculate_damage, fight
from game.monster import Monster
from game.player import Player


class CombatTests(unittest.TestCase):
    def test_calculate_damage_has_minimum_one(self) -> None:
        self.assertEqual(calculate_damage(3, 10), 1)

    def test_fight_rewards_player_on_victory(self) -> None:
        player = Player(name="Tester", hp=30, max_hp=30, attack=8, defense=3)
        monster = Monster(
            name="Training Dummy",
            hp=6,
            attack=1,
            defense=0,
            exp_reward=5,
            gold_reward=3,
        )

        victory, log = fight(player, monster)

        self.assertTrue(victory)
        self.assertEqual(player.exp, 5)
        self.assertEqual(player.gold, 3)
        self.assertTrue(any("defeated" in line for line in log))


if __name__ == "__main__":
    unittest.main()
