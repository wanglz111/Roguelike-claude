from cli.renderer import render_inventory


def prompt_player_name() -> str:
    name = input("Enter your hero name: ").strip()
    return name or "Hero"


def confirm_start() -> bool:
    choice = input("Start the tower run? [Y/n]: ").strip().lower()
    return choice in {"", "y", "yes"}


def prompt_item_use(player) -> str:
    if not player.inventory:
        return ""
    print(f"\nHP: {player.hp}/{player.max_hp}")
    render_inventory(player)
    choice = input("Use item? (number or Enter to continue): ").strip()
    return choice
