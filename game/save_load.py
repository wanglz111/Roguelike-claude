"""Save and load game state to/from JSON files."""
import json
import os
from pathlib import Path
from typing import Optional

from game.game_state import GameState
from game.player import Player
from game.item import Item
from game.i18n import t


SAVE_DIR = Path.home() / ".roguelike_saves"
SAVE_FILE = "save.json"


def ensure_save_dir() -> Path:
    """Ensure save directory exists and return its path."""
    SAVE_DIR.mkdir(parents=True, exist_ok=True)
    return SAVE_DIR


def save_game(state: GameState) -> str:
    """Save game state to JSON file.

    Args:
        state: Current game state to save

    Returns:
        Success or error message
    """
    try:
        save_dir = ensure_save_dir()
        save_path = save_dir / SAVE_FILE

        # Serialize player inventory and equipment
        inventory_data = []
        for item in state.player.inventory:
            inventory_data.append({
                "name": item.name,
                "item_type": item.item_type,
                "effect_type": item.effect_type,
                "effect_value": item.effect_value,
                "description": item.description,
                "equipment_slot": item.equipment_slot,
                "bonus_attack": item.bonus_attack,
                "bonus_defense": item.bonus_defense,
                "bonus_hp": item.bonus_hp,
            })

        weapon_data = None
        if state.player.weapon:
            weapon_data = {
                "name": state.player.weapon.name,
                "item_type": state.player.weapon.item_type,
                "effect_type": state.player.weapon.effect_type,
                "effect_value": state.player.weapon.effect_value,
                "description": state.player.weapon.description,
                "equipment_slot": state.player.weapon.equipment_slot,
                "bonus_attack": state.player.weapon.bonus_attack,
                "bonus_defense": state.player.weapon.bonus_defense,
                "bonus_hp": state.player.weapon.bonus_hp,
            }

        armor_data = None
        if state.player.armor:
            armor_data = {
                "name": state.player.armor.name,
                "item_type": state.player.armor.item_type,
                "effect_type": state.player.armor.effect_type,
                "effect_value": state.player.armor.effect_value,
                "description": state.player.armor.description,
                "equipment_slot": state.player.armor.equipment_slot,
                "bonus_attack": state.player.armor.bonus_attack,
                "bonus_defense": state.player.armor.bonus_defense,
                "bonus_hp": state.player.armor.bonus_hp,
            }

        accessory_data = None
        if state.player.accessory:
            accessory_data = {
                "name": state.player.accessory.name,
                "item_type": state.player.accessory.item_type,
                "effect_type": state.player.accessory.effect_type,
                "effect_value": state.player.accessory.effect_value,
                "description": state.player.accessory.description,
                "equipment_slot": state.player.accessory.equipment_slot,
                "bonus_attack": state.player.accessory.bonus_attack,
                "bonus_defense": state.player.accessory.bonus_defense,
                "bonus_hp": state.player.accessory.bonus_hp,
            }

        # Build save data
        save_data = {
            "player": {
                "name": state.player.name,
                "max_hp": state.player.max_hp,
                "hp": state.player.hp,
                "max_mp": state.player.max_mp,
                "mp": state.player.mp,
                "attack": state.player.attack,
                "defense": state.player.defense,
                "level": state.player.level,
                "exp": state.player.exp,
                "gold": state.player.gold,
                "inventory": inventory_data,
                "weapon": weapon_data,
                "armor": armor_data,
                "accessory": accessory_data,
                "player_class": state.player.player_class,
                "hp_per_level": state.player.hp_per_level,
                "mp_per_level": state.player.mp_per_level,
                "attack_per_level": state.player.attack_per_level,
                "defense_per_level": state.player.defense_per_level,
            },
            "floor": state.floor,
            "max_floor": state.max_floor,
            "game_over": state.game_over,
            "log": state.log,
            "cycle": state.cycle,
        }

        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, ensure_ascii=False, indent=2)

        return t({"en": f"Game saved to {save_path}", "zh": f"游戏已保存到 {save_path}"})

    except Exception as e:
        return t({"en": f"Failed to save game: {e}", "zh": f"保存游戏失败：{e}"})


def load_game() -> tuple[Optional[GameState], str]:
    """Load game state from JSON file.

    Returns:
        Tuple of (GameState or None, message)
    """
    try:
        save_dir = ensure_save_dir()
        save_path = save_dir / SAVE_FILE

        if not save_path.exists():
            return None, t({"en": "No save file found.", "zh": "未找到存档文件。"})

        with open(save_path, 'r', encoding='utf-8') as f:
            save_data = json.load(f)

        # Deserialize inventory
        inventory = []
        for item_data in save_data["player"]["inventory"]:
            inventory.append(Item(**item_data))

        # Deserialize equipment
        weapon = None
        if save_data["player"]["weapon"]:
            weapon = Item(**save_data["player"]["weapon"])

        armor = None
        if save_data["player"]["armor"]:
            armor = Item(**save_data["player"]["armor"])

        accessory = None
        if save_data["player"].get("accessory"):
            accessory = Item(**save_data["player"]["accessory"])

        # Reconstruct player
        player = Player(
            name=save_data["player"]["name"],
            max_hp=save_data["player"]["max_hp"],
            hp=save_data["player"]["hp"],
            max_mp=save_data["player"].get("max_mp", 20),
            mp=save_data["player"].get("mp", 20),
            attack=save_data["player"]["attack"],
            defense=save_data["player"]["defense"],
            level=save_data["player"]["level"],
            exp=save_data["player"]["exp"],
            gold=save_data["player"]["gold"],
            inventory=inventory,
            weapon=weapon,
            armor=armor,
            accessory=accessory,
            player_class=save_data["player"].get("player_class", "rogue"),
            hp_per_level=save_data["player"].get("hp_per_level", 6),
            mp_per_level=save_data["player"].get("mp_per_level", 5),
            attack_per_level=save_data["player"].get("attack_per_level", 2),
            defense_per_level=save_data["player"].get("defense_per_level", 1),
        )

        # Reconstruct game state
        state = GameState(
            player=player,
            floor=save_data["floor"],
            max_floor=save_data["max_floor"],
            game_over=save_data["game_over"],
            log=save_data["log"],
            cycle=save_data.get("cycle", 1),
        )

        return state, t({"en": f"Game loaded from {save_path}", "zh": f"游戏已从 {save_path} 加载"})

    except Exception as e:
        return None, t({"en": f"Failed to load game: {e}", "zh": f"加载游戏失败：{e}"})


def has_save_file() -> bool:
    """Check if a save file exists."""
    save_path = SAVE_DIR / SAVE_FILE
    return save_path.exists()
