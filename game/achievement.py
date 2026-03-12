"""Achievement system for tracking player accomplishments."""

from dataclasses import dataclass
from typing import List, Dict
import json
import os


@dataclass
class Achievement:
    """Represents a single achievement."""
    id: str
    name_en: str
    name_zh: str
    description_en: str
    description_zh: str
    category: str  # combat, exploration, collection, progression
    hidden: bool = False  # Hidden achievements don't show until unlocked


def load_achievements() -> List[Achievement]:
    """Load all achievements from JSON file."""
    json_path = os.path.join(os.path.dirname(__file__), "..", "content", "achievements.json")
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    achievements = []
    for ach_data in data["achievements"]:
        achievement = Achievement(
            id=ach_data["id"],
            name_en=ach_data["name_en"],
            name_zh=ach_data["name_zh"],
            description_en=ach_data["description_en"],
            description_zh=ach_data["description_zh"],
            category=ach_data["category"],
            hidden=ach_data.get("hidden", False)
        )
        achievements.append(achievement)

    return achievements


def get_achievement_by_id(achievements: List[Achievement], achievement_id: str) -> Achievement:
    """Get a specific achievement by ID."""
    for ach in achievements:
        if ach.id == achievement_id:
            return ach
    return None
