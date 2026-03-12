import random

from cli.input_handler import confirm_start, prompt_player_name, prompt_item_use
from cli.renderer import render_intro, render_state
from game.combat import fight
from game.floor import generate_monster, load_items
from game.game_state import GameState
from game.player import Player
from game.i18n import get_i18n, t


def main() -> None:
    # Language selection
    lang_choice = input("Select language / 选择语言 [en/zh]: ").strip().lower()
    if lang_choice in {"zh", "中文", "中"}:
        get_i18n().set_language("zh")
    else:
        get_i18n().set_language("en")

    render_intro()
    if not confirm_start():
        print(t({"en": "Run cancelled.", "zh": "运行已取消。"}))
        return

    name = prompt_player_name()
    state = GameState(player=Player(name=name))

    rng = random.Random(42)
    items_db = load_items()
    state.log.append(t({"en": f"Welcome, {state.player.name}.", "zh": f"欢迎，{state.player.name}。"}))

    while not state.game_over and state.floor <= state.max_floor:
        state.log.append(t({"en": f"Floor {state.floor} begins.", "zh": f"第{state.floor}层开始。"}))
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
            state.log.append(t({"en": "You cleared the tower prototype.", "zh": "你通关了塔楼原型。"}))
            state.game_over = True
            break

        choice = prompt_item_use(state.player)
        if choice.isdigit():
            idx = int(choice) - 1
            msg = state.player.use_item(idx)
            state.log.append(msg)

        state.floor += 1
        state.log.append(t({"en": "You descend to the next floor.", "zh": "你下到了下一层。"}))

    render_state(state)


if __name__ == "__main__":
    main()
