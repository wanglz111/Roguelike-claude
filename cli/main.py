import random

from cli.input_handler import confirm_start, prompt_player_name, prompt_item_use, prompt_event_choice, prompt_shop_purchase, prompt_skill_use, prompt_class_selection, prompt_view_achievements
from cli.renderer import render_intro, render_state
from game.combat import fight
from game.floor import generate_monster, load_items, generate_event, generate_shop
from game.game_state import GameState
from game.player import Player
from game.player_class import load_classes
from game.skill import load_skills
from game.achievement import load_achievements
from game.achievement_checker import check_achievements, format_achievement_unlock
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

        # Load classes and prompt for class selection
        classes_db = load_classes()
        class_id = prompt_class_selection(classes_db)
        selected_class = classes_db[class_id]

        # Create player with class-specific stats
        state = GameState(player=Player(
            name=name,
            max_hp=selected_class.base_hp,
            hp=selected_class.base_hp,
            max_mp=selected_class.base_mp,
            mp=selected_class.base_mp,
            attack=selected_class.base_attack,
            defense=selected_class.base_defense,
            player_class=class_id,
            hp_per_level=selected_class.hp_per_level,
            mp_per_level=selected_class.mp_per_level,
            attack_per_level=selected_class.attack_per_level,
            defense_per_level=selected_class.defense_per_level
        ))

        print(t({"en": f"\nYou are now a {selected_class.get_name()}!", "zh": f"\n你现在是一名{selected_class.get_name()}！"}))
        input(t({"en": "Press Enter to begin your adventure...", "zh": "按回车开始你的冒险..."}))


    rng = random.Random()
    items_db = load_items()
    skills_db = load_skills()
    achievements_db = load_achievements()
    state.log.append(t({"en": f"Welcome, {state.player.name}.", "zh": f"欢迎，{state.player.name}。"}))

    while not state.game_over and state.floor <= state.max_floor:
        state.log.append(t({"en": f"Floor {state.floor} begins.", "zh": f"第{state.floor}层开始。"}))

        # Check floor achievement
        newly_unlocked = check_achievements(state.player, achievements_db, "floor_reached", floor=state.floor)
        for _, ach in newly_unlocked:
            print(format_achievement_unlock(ach))

        monster = generate_monster(state.floor, rng, state.cycle)

        # Prompt for skill usage
        skill_id = prompt_skill_use(state.player, skills_db)
        skill = None
        if skill_id:
            skill = skills_db[skill_id]
            state.player.mp -= skill.mp_cost
            state.player.skills_used += 1

            # Check skill usage achievement
            newly_unlocked = check_achievements(state.player, achievements_db, "skill_used")
            for _, ach in newly_unlocked:
                print(format_achievement_unlock(ach))

        player_hp_before = state.player.hp
        victory, battle_log = fight(state.player, monster, skill)
        state.log.extend(battle_log)

        if not victory:
            state.game_over = True
            break

        # Track monster kills
        state.player.monsters_killed += 1
        if monster.is_boss:
            state.player.bosses_killed += 1

        # Check combat achievements
        damage_taken = player_hp_before - state.player.hp
        newly_unlocked = check_achievements(state.player, achievements_db, "monster_killed",
                                           is_boss=monster.is_boss, monster_name=monster.get_name())
        for _, ach in newly_unlocked:
            print(format_achievement_unlock(ach))

        newly_unlocked = check_achievements(state.player, achievements_db, "battle_won",
                                           is_boss=monster.is_boss, damage_taken=damage_taken)
        for _, ach in newly_unlocked:
            print(format_achievement_unlock(ach))

        if not victory:
            state.game_over = True
            break

        if monster.drop_item and monster.drop_item in items_db:
            item = items_db[monster.drop_item]
            msg = state.player.add_item(item)
            state.log.append(msg)

        # Check gold achievement
        newly_unlocked = check_achievements(state.player, achievements_db, "gold_changed")
        for _, ach in newly_unlocked:
            print(format_achievement_unlock(ach))

        # Check level up achievement
        newly_unlocked = check_achievements(state.player, achievements_db, "level_up")
        for _, ach in newly_unlocked:
            print(format_achievement_unlock(ach))

        if state.floor == state.max_floor:
            state.log.append(t({"en": "You cleared the tower prototype.", "zh": "你通关了塔楼原型。"}))

            # Check completion achievement
            newly_unlocked = check_achievements(state.player, achievements_db, "floor_reached", floor=state.floor + 1)
            for _, ach in newly_unlocked:
                print(format_achievement_unlock(ach))

            render_state(state)

            # Offer New Game+
            ng_choice = input(t({"en": f"\nStart New Game+ (Cycle {state.cycle + 1})? [Y/n]: ", "zh": f"\n开始新周目（第{state.cycle + 1}周）？[Y/n]："})).strip().lower()
            if ng_choice in {"", "y", "yes", "是"}:
                # Check New Game+ achievement
                newly_unlocked = check_achievements(state.player, achievements_db, "new_game_plus")
                for _, ach in newly_unlocked:
                    print(format_achievement_unlock(ach))

                # Start New Game+
                state.cycle += 1
                state.floor = 1
                state.game_over = False
                state.log = []
                state.player.hp = state.player.max_hp
                state.player.mp = state.player.max_mp
                state.player.gold = state.player.gold // 2  # Keep half gold
                state.log.append(t({"en": f"New Game+ Cycle {state.cycle} begins! Monster difficulty increased.", "zh": f"新周目第{state.cycle}周开始！怪物难度提升。"}))
                continue
            else:
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
                        state.player.items_purchased += 1
                        item = items_db[item_name]
                        msg = state.player.add_item(item)
                        state.log.append(t({"en": f"Purchased {item.get_name()} for {shop_item.price} gold.", "zh": f"花费{shop_item.price}金币购买了{item.get_name()}。"}))
                        print(msg)

                        # Check purchase achievement
                        newly_unlocked = check_achievements(state.player, achievements_db, "item_purchased")
                        for _, ach in newly_unlocked:
                            print(format_achievement_unlock(ach))

        choice = prompt_item_use(state.player)
        if choice.startswith('u') and choice[1:].isdigit():
            idx = int(choice[1:]) - 1
            msg = state.player.use_item(idx)
            state.log.append(msg)
        elif choice.startswith('e') and choice[1:].isdigit():
            idx = int(choice[1:]) - 1
            item = state.player.inventory[idx] if 0 <= idx < len(state.player.inventory) else None
            msg = state.player.equip_item(idx)
            state.log.append(msg)

            # Check equipment achievements
            if item:
                newly_unlocked = check_achievements(state.player, achievements_db, "equipment_equipped", item=item)
                for _, ach in newly_unlocked:
                    print(format_achievement_unlock(ach))
        elif choice.lower() in {'a', 'achievement', 'achievements'}:
            prompt_view_achievements(state.player, achievements_db)
        elif choice.lower() in {'s', 'save'}:
            msg = save_game(state)
            print(msg)

        state.floor += 1
        state.log.append(t({"en": "You descend to the next floor.", "zh": "你下到了下一层。"}))

    render_state(state)


if __name__ == "__main__":
    main()
