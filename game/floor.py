import json
import random
from pathlib import Path

from game.monster import Monster
from game.item import Item


CONTENT_PATH = Path(__file__).resolve().parent.parent / "content" / "monsters.json"
ITEMS_PATH = Path(__file__).resolve().parent.parent / "content" / "items.json"


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
