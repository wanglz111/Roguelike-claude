import unittest

from game.player import Player
from game.item import Item


class TestInventory(unittest.TestCase):
    def test_add_item(self):
        player = Player(name="Test")
        item = Item("Potion", "consumable", "heal", 15, "Heals 15 HP")
        player.add_item(item)
        self.assertEqual(len(player.inventory), 1)
        self.assertEqual(player.inventory[0].name, "Potion")

    def test_use_heal_item(self):
        player = Player(name="Test", hp=10, max_hp=30)
        item = Item("Potion", "consumable", "heal", 15, "Heals 15 HP")
        player.add_item(item)
        player.use_item(0)
        self.assertEqual(player.hp, 25)
        self.assertEqual(len(player.inventory), 0)

    def test_use_heal_item_max_hp(self):
        player = Player(name="Test", hp=20, max_hp=30)
        item = Item("Potion", "consumable", "heal", 15, "Heals 15 HP")
        player.add_item(item)
        player.use_item(0)
        self.assertEqual(player.hp, 30)


if __name__ == "__main__":
    unittest.main()
