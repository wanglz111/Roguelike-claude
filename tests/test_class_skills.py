"""Test class-specific skills."""
from game.skill import load_skills
from game.player import Player


def test_class_specific_skills_exist():
    """Test that class-specific skills are loaded correctly."""
    skills = load_skills()

    # Warrior skills
    assert "shield_bash" in skills
    assert skills["shield_bash"].class_required == "warrior"
    assert "iron_will" in skills
    assert skills["iron_will"].class_required == "warrior"

    # Mage skills
    assert "fireball" in skills
    assert skills["fireball"].class_required == "mage"
    assert "mana_surge" in skills
    assert skills["mana_surge"].class_required == "mage"

    # Rogue skills
    assert "backstab" in skills
    assert skills["backstab"].class_required == "rogue"
    assert "evasion" in skills
    assert skills["evasion"].class_required == "rogue"


def test_universal_skills_have_no_class_requirement():
    """Test that universal skills have no class requirement."""
    skills = load_skills()

    assert skills["power_strike"].class_required is None
    assert skills["heal"].class_required is None
    assert skills["defend"].class_required is None
