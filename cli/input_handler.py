def prompt_player_name() -> str:
    name = input("Enter your hero name: ").strip()
    return name or "Hero"


def confirm_start() -> bool:
    choice = input("Start the tower run? [Y/n]: ").strip().lower()
    return choice in {"", "y", "yes"}
