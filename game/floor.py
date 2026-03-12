import json
import random
from pathlib import Path

from game.monster import Monster
from game.item import Item
from game.event import Event, EventChoice


CONTENT_PATH = Path(__file__).resolve().parent.parent / "content" / "monsters.json"
ITEMS_PATH = Path(__file__).resolve().parent.parent / "content" / "items.json"
EVENTS_PATH = Path(__file__).resolve().parent.parent / "content" / "events.json"


def load_monster_pool() -> list[dict]:
    with CONTENT_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_items() -> dict[str, Item]:
    with ITEMS_PATH.open("r", encoding="utf-8") as handle:
        items_data = json.load(handle)
        # Use English name as key for backward compatibility
        result = {}
        for item_data in items_data:
            item = Item(**item_data)
            # Use English name as dictionary key
            key = item_data["name"]["en"] if isinstance(item_data["name"], dict) else item_data["name"]
            result[key] = item
        return result


def load_events() -> list[dict]:
    with EVENTS_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def generate_monster(floor: int, rng: random.Random) -> Monster:
    candidates = [
        monster for monster in load_monster_pool() if monster["min_floor"] <= floor
    ]
    template = rng.choice(candidates)
    scale = max(0, floor - template["min_floor"])
    return Monster(
        name=template["name"],
        hp=template["hp"] + scale * 2,
        attack=template["attack"] + scale,
        defense=template["defense"] + scale // 2,
        exp_reward=template["exp_reward"] + scale * 2,
        gold_reward=template["gold_reward"] + scale,
        drop_item=template.get("drop_item"),
    )


def generate_event(floor: int, rng: random.Random) -> Event | None:
    """Generate a random event for the current floor.

    Returns None if no event should occur (50% chance).
    """
    if rng.random() > 0.5:
        return None

    candidates = [
        event for event in load_events() if event["min_floor"] <= floor
    ]

    if not candidates:
        return None

    template = rng.choice(candidates)
    choices = [EventChoice(**choice) for choice in template["choices"]]

    return Event(
        name=template["name"],
        description=template["description"],
        choices=choices,
        min_floor=template["min_floor"]
    )
