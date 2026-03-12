import unittest
from game.player import Player
from game.item import Item


class TestEquipment(unittest.TestCase):
    def test_equip_weapon(self):
        player = Player(name="Test")
        sword = Item(
            name="Sword",
            item_type="equipment",
            effect_type="none",
            effect_value=0,
            description="A sword",
            equipment_slot="weapon",
            bonus_attack=5,
            bonus_defense=0,
            bonus_hp=0
        )
        player.inventory.append(sword)

        base_attack = player.attack
        player.equip_item(0)

        self.assertEqual(player.total_attack, base_attack + 5)
        self.assertIsNotNone(player.weapon)
        self.assertEqual(len(player.inventory), 0)

    def test_equip_armor(self):
        player = Player(name="Test")
        armor = Item(
            name="Armor",
            item_type="equipment",
            effect_type="none",
            effect_value=0,
            description="An armor",
            equipment_slot="armor",
            bonus_attack=0,
            bonus_defense=3,
            bonus_hp=10
        )
        player.inventory.append(armor)

        base_defense = player.defense
        base_hp = player.max_hp
        player.equip_item(0)

        self.assertEqual(player.total_defense, base_defense + 3)
        self.assertEqual(player.total_max_hp, base_hp + 10)
        self.assertIsNotNone(player.armor)

    def test_replace_equipment(self):
        player = Player(name="Test")
        sword1 = Item(
            name="Sword1",
            item_type="equipment",
            effect_type="none",
            effect_value=0,
            description="First sword",
            equipment_slot="weapon",
            bonus_attack=3,
            bonus_defense=0,
            bonus_hp=0
        )
        sword2 = Item(
            name="Sword2",
            item_type="equipment",
            effect_type="none",
            effect_value=0,
            description="Second sword",
            equipment_slot="weapon",
            bonus_attack=5,
            bonus_defense=0,
            bonus_hp=0
        )

        player.inventory.append(sword1)
        player.equip_item(0)
        player.inventory.append(sword2)
        player.equip_item(0)

        self.assertEqual(player.total_attack, player.attack + 5)
        self.assertEqual(len(player.inventory), 1)


if __name__ == "__main__":
    unittest.main()
