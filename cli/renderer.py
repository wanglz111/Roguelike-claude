from game.game_state import GameState


def render_intro() -> None:
    print("== Tower Prototype ==")
    print("A minimal CLI roguelike built for AI-driven iterative development.")


def render_inventory(player) -> None:
    if not player.inventory:
        print("Inventory: (empty)")
        return
    print("Inventory:")
    for i, item in enumerate(player.inventory):
        print(f"  {i+1}. {item.name} - {item.description}")


def render_state(state: GameState) -> None:
    print()
    print("== Final Summary ==")
    print(
        f"{state.player.name} | Level {state.player.level} | "
        f"HP {state.player.hp}/{state.player.max_hp} | Gold {state.player.gold}"
    )
    print(f"Reached floor: {state.floor}")
    render_inventory(state.player)
    print()
    print("== Run Log ==")
    for entry in state.log:
        print(f"- {entry}")
