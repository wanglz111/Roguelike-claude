import random

from cli.input_handler import confirm_start, prompt_player_name, prompt_item_use
from cli.renderer import render_intro, render_state
from game.combat import fight
from game.floor import generate_monster, load_items
from game.game_state import GameState
from game.player import Player


def main() -> None:
    render_intro()
    if not confirm_start():
        print("Run cancelled.")
        return

    name = prompt_player_name()
    state = GameState(player=Player(name=name))

    rng = random.Random(42)
    items_db = load_items()
    state.log.append(f"Welcome, {state.player.name}.")

    while not state.game_over and state.floor <= state.max_floor:
        state.log.append(f"Floor {state.floor} begins.")
        monster = generate_monster(state.floor, rng)
        victory, battle_log = fight(state.player, monster)
        state.log.extend(battle_log)

        if not victory:
            state.game_over = True
            break

        if monster.drop_item and monster.drop_item in items_db:
            item = items_db[monster.drop_item]
            msg = state.player.add_item(item)
            state.log.append(msg)

        if state.floor == state.max_floor:
            state.log.append("You cleared the tower prototype.")
            state.game_over = True
            break

        choice = prompt_item_use(state.player)
        if choice.isdigit():
            idx = int(choice) - 1
            msg = state.player.use_item(idx)
            state.log.append(msg)

        state.floor += 1
        state.log.append("You descend to the next floor.")

    render_state(state)


if __name__ == "__main__":
    main()
