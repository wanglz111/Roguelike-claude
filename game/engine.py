import random

from game.combat import fight
from game.floor import generate_monster
from game.game_state import GameState


def run_game(state: GameState, seed: int = 42) -> GameState:
    rng = random.Random(seed)
    state.log.append(f"Welcome, {state.player.name}.")

    while not state.game_over and state.floor <= state.max_floor:
        state.log.append(f"Floor {state.floor} begins.")
        monster = generate_monster(state.floor, rng)
        victory, battle_log = fight(state.player, monster)
        state.log.extend(battle_log)

        if not victory:
            state.game_over = True
            break

        if state.floor == state.max_floor:
            state.log.append("You cleared the tower prototype.")
            state.game_over = True
            break

        state.floor += 1
        state.log.append("You descend to the next floor.")

    return state
