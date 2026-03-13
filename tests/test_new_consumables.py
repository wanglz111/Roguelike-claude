import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game.player import Player
from game.item import Item
from game.player_class import PlayerClass
from game.status_effect import StatusEffect, ActiveStatusEffect


def test_restore_both():
    """Test Elixir of Vitality restores both HP and MP."""
    player_class = PlayerClass("Warrior", {"en": "Warrior", "zh": "战士"}, 100, 30, 10, 5, 10, 3, 2, 1)
    player = Player("Test", player_class)
    player.hp = 50
    player.mp = 10

    elixir = Item(
        name={"en": "Elixir of Vitality", "zh": "活力药剂"},
        item_type="consumable",
        effect_type="restore_both",
        effect_value=25,
        description={"en": "Restores 25 HP and 25 MP", "zh": "恢复25点生命值和25点魔力值"}
    )
    player.add_item(elixir)
    result = player.use_item(0)

    assert player.hp == 75
    assert player.mp == 35
    assert "25" in result


def test_cure_status():
    """Test Antidote removes status effects."""
    player_class = PlayerClass("Warrior", {"en": "Warrior", "zh": "战士"}, 100, 30, 10, 5, 10, 3, 2, 1)
    player = Player("Test", player_class)

    poison = StatusEffect("poison", {"en": "Poison", "zh": "中毒"}, {"en": "Takes damage", "zh": "持续伤害"}, "poison", 3, 3, 1.0, 1.0)
    player.add_status_effect(ActiveStatusEffect(poison, 3))

    antidote = Item(
        name={"en": "Antidote", "zh": "解毒剂"},
        item_type="consumable",
        effect_type="cure_status",
        effect_value=0,
        description={"en": "Removes all negative status effects", "zh": "移除所有负面状态效果"}
    )
    player.add_item(antidote)
    result = player.use_item(0)

    assert len(player.status_effects) == 0
    assert "1" in result


def test_full_restore():
    """Test Scroll of Sanctuary fully restores HP and MP."""
    player_class = PlayerClass("Warrior", {"en": "Warrior", "zh": "战士"}, 100, 30, 10, 5, 10, 3, 2, 1)
    player = Player("Test", player_class)
    player.hp = 20
    player.mp = 5

    scroll = Item(
        name={"en": "Scroll of Sanctuary", "zh": "庇护卷轴"},
        item_type="consumable",
        effect_type="full_restore",
        effect_value=0,
        description={"en": "Fully restores HP and MP", "zh": "完全恢复生命值和魔力值"}
    )
    player.add_item(scroll)
    result = player.use_item(0)

    assert player.hp == player.total_max_hp
    assert player.mp == player.total_max_mp


if __name__ == "__main__":
    test_restore_both()
    print("✓ test_restore_both passed")

    test_cure_status()
    print("✓ test_cure_status passed")

    test_full_restore()
    print("✓ test_full_restore passed")

    print("\nAll new consumable tests passed!")
