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
        print(f"\n{t({'en': 'HP', 'zh': '生命值'})}: {player.hp}/{player.total_max_hp}")
        choice = input(t({"en": "Press Enter to continue or 's' to save: ", "zh": "按回车继续或输入's'保存："})).strip()
        return choice
    print(f"\n{t({'en': 'HP', 'zh': '生命值'})}: {player.hp}/{player.total_max_hp}")
    render_inventory(player)
    choice = input(t({"en": "Use item (u<number>) or Equip (e<number>) or 's' to save or Enter to continue: ", "zh": "使用物品（u数字）或装备（e数字）或输入's'保存或回车继续："})).strip()
    return choice


def prompt_event_choice(event) -> int:
    """Prompt player to choose an event option.

    Returns:
        Index of the chosen option (0-based)
    """
    print(f"\n=== {event.get_name()} ===")
    print(event.get_description())
    print()
    for i, choice in enumerate(event.choices, 1):
        print(f"{i}. {choice.get_text()}")
    print()

    while True:
        choice = input(t({"en": "Choose an option: ", "zh": "选择一个选项："})).strip()
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(event.choices):
                return idx
        print(t({"en": "Invalid choice. Try again.", "zh": "无效的选择。请重试。"}))
