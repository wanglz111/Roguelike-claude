from game.game_state import GameState


def render_intro() -> None:
    print("== Tower Prototype ==")
    print("A minimal CLI roguelike built for AI-driven iterative development.")


def render_state(state: GameState) -> None:
    print()
    print("== Final Summary ==")
    print(
        f"{state.player.name} | Level {state.player.level} | "
        f"HP {state.player.hp}/{state.player.max_hp} | Gold {state.player.gold}"
    )
    print(f"Reached floor: {state.floor}")
    print()
    print("== Run Log ==")
    for entry in state.log:
        print(f"- {entry}")
