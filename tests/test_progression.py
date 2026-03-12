import unittest

from game.player import Player


class ProgressionTests(unittest.TestCase):
    def test_player_levels_up_and_restores_hp(self) -> None:
        player = Player(
            name="Tester",
            hp=7,
            max_hp=30,
            attack=8,
            defense=3,
            level=1,
            exp=0,
        )

        messages = player.gain_rewards(exp=10, gold=5)

        self.assertEqual(player.level, 2)
        self.assertEqual(player.hp, player.max_hp)
        self.assertEqual(player.gold, 5)
        self.assertTrue(any("Level up!" in message for message in messages))


if __name__ == "__main__":
    unittest.main()
