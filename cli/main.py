from cli.input_handler import confirm_start, prompt_player_name
from cli.renderer import render_intro, render_state
from game.engine import run_game
from game.game_state import GameState
from game.player import Player


def main() -> None:
    render_intro()
    if not confirm_start():
        print("Run cancelled.")
        return

    name = prompt_player_name()
    state = GameState(player=Player(name=name))
    final_state = run_game(state)
    render_state(final_state)


if __name__ == "__main__":
    main()
