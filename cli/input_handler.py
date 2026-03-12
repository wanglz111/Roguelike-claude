from cli.renderer import render_inventory
from game.i18n import t


def prompt_player_name() -> str:
    name = input(t({"en": "Enter your hero name: ", "zh": "输入你的英雄名字："})).strip()
    return name or t({"en": "Hero", "zh": "英雄"})


def confirm_start() -> bool:
    choice = input(t({"en": "Start the tower run? [Y/n]: ", "zh": "开始塔楼冒险？[Y/n]："})).strip().lower()
    return choice in {"", "y", "yes"}


def prompt_item_use(player) -> str:
    if not player.inventory:
        return ""
    print(f"\n{t({'en': 'HP', 'zh': '生命值'})}: {player.hp}/{player.total_max_hp}")
    render_inventory(player)
    choice = input(t({"en": "Use item (u<number>) or Equip (e<number>) or Enter to continue: ", "zh": "使用物品（u数字）或装备（e数字）或回车继续："})).strip()
    return choice
