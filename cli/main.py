import random

from cli.input_handler import confirm_start, prompt_player_name, prompt_item_use, prompt_event_choice, prompt_shop_purchase
from cli.renderer import render_intro, render_state
from game.combat import fight
from game.floor import generate_monster, load_items, generate_event, generate_shop
from game.game_state import GameState
from game.player import Player
from game.i18n import get_i18n, t
from game.save_load import save_game, load_game, has_save_file


def main() -> None:
    # Language selection
    lang_choice = input("Select language / 选择语言 [en/zh]: ").strip().lower()
    if lang_choice in {"zh", "中文", "中"}:
        get_i18n().set_language("zh")
    else:
        get_i18n().set_language("en")

    render_intro()

    # Check for existing save file
    state = None
    if has_save_file():
        load_choice = input(t({"en": "Load saved game? [Y/n]: ", "zh": "加载存档？[Y/n]："})).strip().lower()
        if load_choice in {"", "y", "yes", "是"}:
            state, msg = load_game()
            print(msg)
            if state is None:
                return

    # Start new game if no save loaded
    if state is None:
        if not confirm_start():
            print(t({"en": "Run cancelled.", "zh": "运行已取消。"}))
            return
        name = prompt_player_name()
        state = GameState(player=Player(name=name))

    rng = random.Random()
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

        # Check for random event
        event = generate_event(state.floor, rng)
        if event:
            choice_idx = prompt_event_choice(event)
            chosen = event.choices[choice_idx]
            extra_msg = state.player.apply_event_effect(chosen.effect_type, chosen.effect_value)
            state.log.append(chosen.get_result_text() + extra_msg)

            # Check if player died from event damage
            if not state.player.is_alive:
                state.log.append(t({"en": "You have fallen...", "zh": "你倒下了……"}))
                state.game_over = True
                break

        # Check for shop
        shop = generate_shop(state.floor, rng)
        if shop:
            while True:
                item_idx, should_leave = prompt_shop_purchase(shop, state.player, items_db)
                if should_leave:
                    state.log.append(t({"en": "You leave the shop.", "zh": "你离开了商店。"}))
                    break
                if item_idx >= 0:
                    shop_item = shop.items[item_idx]
                    if not shop_item.is_available():
                        print(t({"en": "That item is out of stock.", "zh": "该物品已售罄。"}))
                        continue
                    if state.player.gold < shop_item.price:
                        print(t({"en": "Not enough gold!", "zh": "金币不足！"}))
                        continue
                    # Purchase successful
                    success, item_name = shop.purchase_item(item_idx)
                    if success and item_name in items_db:
                        state.player.gold -= shop_item.price
                        item = items_db[item_name]
                        msg = state.player.add_item(item)
                        state.log.append(t({"en": f"Purchased {item.get_name()} for {shop_item.price} gold.", "zh": f"花费{shop_item.price}金币购买了{item.get_name()}。"}))
                        print(msg)

        choice = prompt_item_use(state.player)
        if choice.startswith('u') and choice[1:].isdigit():
            idx = int(choice[1:]) - 1
            msg = state.player.use_item(idx)
            state.log.append(msg)
        elif choice.startswith('e') and choice[1:].isdigit():
            idx = int(choice[1:]) - 1
            msg = state.player.equip_item(idx)
            state.log.append(msg)
        elif choice.lower() in {'s', 'save'}:
            msg = save_game(state)
            print(msg)

        state.floor += 1
        state.log.append(t({"en": "You descend to the next floor.", "zh": "你下到了下一层。"}))

    render_state(state)


if __name__ == "__main__":
    main()
