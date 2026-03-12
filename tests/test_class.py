import unittest
from game.player import Player
from game.player_class import load_classes, PlayerClass


class ClassTests(unittest.TestCase):
    def test_load_classes(self):
        """Test that classes load correctly from JSON."""
        classes = load_classes()

        self.assertEqual(len(classes), 3)
        self.assertIn("warrior", classes)
        self.assertIn("mage", classes)
        self.assertIn("rogue", classes)

    def test_warrior_class(self):
        """Test warrior class stats."""
        classes = load_classes()
        warrior = classes["warrior"]

        self.assertEqual(warrior.class_id, "warrior")
        self.assertEqual(warrior.base_hp, 35)
        self.assertEqual(warrior.base_mp, 15)
        self.assertEqual(warrior.base_attack, 10)
        self.assertEqual(warrior.base_defense, 4)
        self.assertEqual(warrior.hp_per_level, 7)
        self.assertEqual(warrior.mp_per_level, 3)
        self.assertEqual(warrior.attack_per_level, 3)
        self.assertEqual(warrior.defense_per_level, 1)

    def test_mage_class(self):
        """Test mage class stats."""
        classes = load_classes()
        mage = classes["mage"]

        self.assertEqual(mage.class_id, "mage")
        self.assertEqual(mage.base_hp, 25)
        self.assertEqual(mage.base_mp, 30)
        self.assertEqual(mage.base_attack, 6)
        self.assertEqual(mage.base_defense, 2)
        self.assertEqual(mage.hp_per_level, 5)
        self.assertEqual(mage.mp_per_level, 8)
        self.assertEqual(mage.attack_per_level, 2)
        self.assertEqual(mage.defense_per_level, 1)

    def test_rogue_class(self):
        """Test rogue class stats."""
        classes = load_classes()
        rogue = classes["rogue"]

        self.assertEqual(rogue.class_id, "rogue")
        self.assertEqual(rogue.base_hp, 30)
        self.assertEqual(rogue.base_mp, 20)
        self.assertEqual(rogue.base_attack, 8)
        self.assertEqual(rogue.base_defense, 3)
        self.assertEqual(rogue.hp_per_level, 6)
        self.assertEqual(rogue.mp_per_level, 5)
        self.assertEqual(rogue.attack_per_level, 2)
        self.assertEqual(rogue.defense_per_level, 1)

    def test_player_with_warrior_class(self):
        """Test creating a player with warrior class."""
        classes = load_classes()
        warrior = classes["warrior"]

        player = Player(
            name="Test Warrior",
            max_hp=warrior.base_hp,
            hp=warrior.base_hp,
            max_mp=warrior.base_mp,
            mp=warrior.base_mp,
            attack=warrior.base_attack,
            defense=warrior.base_defense,
            player_class="warrior",
            hp_per_level=warrior.hp_per_level,
            mp_per_level=warrior.mp_per_level,
            attack_per_level=warrior.attack_per_level,
            defense_per_level=warrior.defense_per_level
        )

        self.assertEqual(player.name, "Test Warrior")
        self.assertEqual(player.max_hp, 35)
        self.assertEqual(player.max_mp, 15)
        self.assertEqual(player.attack, 10)
        self.assertEqual(player.defense, 4)
        self.assertEqual(player.player_class, "warrior")

    def test_player_class_growth(self):
        """Test that player stats grow according to class growth rates."""
        classes = load_classes()
        mage = classes["mage"]

        player = Player(
            name="Test Mage",
            max_hp=mage.base_hp,
            hp=mage.base_hp,
            max_mp=mage.base_mp,
            mp=mage.base_mp,
            attack=mage.base_attack,
            defense=mage.base_defense,
            player_class="mage",
            hp_per_level=mage.hp_per_level,
            mp_per_level=mage.mp_per_level,
            attack_per_level=mage.attack_per_level,
            defense_per_level=mage.defense_per_level
        )

        initial_hp = player.max_hp
        initial_mp = player.max_mp
        initial_attack = player.attack
        initial_defense = player.defense

        # Gain enough exp to level up once (level 1 needs 10 exp)
        player.gain_rewards(10, 0)

        # Check that stats increased by class growth rates
        self.assertEqual(player.max_hp, initial_hp + mage.hp_per_level)
        self.assertEqual(player.max_mp, initial_mp + mage.mp_per_level)
        self.assertEqual(player.attack, initial_attack + mage.attack_per_level)
        self.assertEqual(player.defense, initial_defense + mage.defense_per_level)
        self.assertEqual(player.level, 2)
