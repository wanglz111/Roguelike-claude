import random

from game.combat import fight
from game.floor import generate_monster, load_items
from game.game_state import GameState


def run_game(state: GameState, seed: int = 42) -> GameState:
    rng = random.Random(seed)
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

        state.floor += 1
        state.log.append("You descend to the next floor.")

    return state
