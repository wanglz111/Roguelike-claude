from cli.renderer import render_inventory
from game.i18n import t


def prompt_view_achievements(player, achievements_db) -> None:
    """Display player's achievements."""
    print(f"\n=== {t({'en': 'Achievements', 'zh': '成就'})} ===")

    # Group achievements by category
    categories = {}
    for ach in achievements_db:
        if ach.category not in categories:
            categories[ach.category] = []
        categories[ach.category].append(ach)

    category_names = {
        "combat": t({"en": "Combat", "zh": "战斗"}),
        "exploration": t({"en": "Exploration", "zh": "探索"}),
        "progression": t({"en": "Progression", "zh": "进度"}),
        "collection": t({"en": "Collection", "zh": "收集"})
    }

    unlocked_count = len(player.unlocked_achievements)
    total_count = len(achievements_db)
    print(f"{t({'en': 'Unlocked', 'zh': '已解锁'})}: {unlocked_count}/{total_count}\n")

    for category, ach_list in categories.items():
        print(f"--- {category_names.get(category, category)} ---")
        for ach in ach_list:
            if ach.id in player.unlocked_achievements:
                name = t({"en": ach.name_en, "zh": ach.name_zh})
                desc = t({"en": ach.description_en, "zh": ach.description_zh})
                print(f"✓ {name}")
                print(f"  {desc}")
            elif not ach.hidden:
                name = t({"en": ach.name_en, "zh": ach.name_zh})
                desc = t({"en": ach.description_en, "zh": ach.description_zh})
                print(f"✗ {name}")
                print(f"  {desc}")
            else:
                print(f"✗ {t({'en': '???', 'zh': '???'})}")
                print(f"  {t({'en': 'Hidden achievement', 'zh': '隐藏成就'})}")
        print()

    # Show stats
    print(f"--- {t({'en': 'Stats', 'zh': '统计'})} ---")
    print(f"{t({'en': 'Monsters killed', 'zh': '击杀怪物'})}: {player.monsters_killed}")
    print(f"{t({'en': 'Bosses defeated', 'zh': '击败Boss'})}: {player.bosses_killed}")
    print(f"{t({'en': 'Skills used', 'zh': '使用技能'})}: {player.skills_used}")
    print(f"{t({'en': 'Items purchased', 'zh': '购买物品'})}: {player.items_purchased}")
    print()

    input(t({"en": "Press Enter to continue...", "zh": "按回车继续..."}))


def prompt_skill_use(player, skills_db) -> str:
    """Prompt player to use a skill before combat.

    Returns:
        skill_id or empty string if no skill used
    """
    print(f"\n{t({'en': 'MP', 'zh': '魔法值'})}: {player.mp}/{player.max_mp}")
    print(t({"en": "Available skills:", "zh": "可用技能："}))

    available_skills = []
    for skill_id, skill in skills_db.items():
        # Filter by class requirement and MP cost
        if skill.class_required and skill.class_required != player.player_class:
            continue
        if player.mp >= skill.mp_cost:
            available_skills.append((skill_id, skill))
            print(f"  {skill_id}: {skill.get_name()} (MP: {skill.mp_cost}) - {skill.get_description()}")

    if not available_skills:
        print(t({"en": "  (Not enough MP for any skill)", "zh": "  （魔法值不足，无法使用技能）"}))
        input(t({"en": "Press Enter to continue...", "zh": "按回车继续..."}))
        return ""

    print()
    choice = input(t({"en": "Use skill (skill_id) or Enter to attack normally: ", "zh": "使用技能（技能ID）或回车普通攻击："})).strip()

    if choice in skills_db:
        skill = skills_db[choice]
        if player.mp >= skill.mp_cost and (not skill.class_required or skill.class_required == player.player_class):
            return choice
    return ""


def prompt_player_name() -> str:
    name = input(t({"en": "Enter your hero name: ", "zh": "输入你的英雄名字："})).strip()
    return name or t({"en": "Hero", "zh": "英雄"})


def prompt_class_selection(classes_db) -> str:
    """Prompt player to select a class.

    Returns:
        class_id of the selected class
    """
    print(t({"en": "\nChoose your class:", "zh": "\n选择你的职业："}))
    print()

    class_list = list(classes_db.items())
    for i, (class_id, player_class) in enumerate(class_list, 1):
        print(f"{i}. {player_class.get_name()}")
        print(f"   {player_class.get_description()}")
        print(f"   HP: {player_class.base_hp} (+{player_class.hp_per_level}/{t({'en': 'level', 'zh': '级'})}), "
              f"MP: {player_class.base_mp} (+{player_class.mp_per_level}/{t({'en': 'level', 'zh': '级'})})")
        print(f"   {t({'en': 'ATK', 'zh': '攻击'})}: {player_class.base_attack} (+{player_class.attack_per_level}/{t({'en': 'level', 'zh': '级'})}), "
              f"{t({'en': 'DEF', 'zh': '防御'})}: {player_class.base_defense} (+{player_class.defense_per_level}/{t({'en': 'level', 'zh': '级'})})")
        print()

    while True:
        choice = input(t({"en": "Select class (1-3): ", "zh": "选择职业（1-3）："})).strip()
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(class_list):
                return class_list[idx][0]
        print(t({"en": "Invalid choice. Try again.", "zh": "无效的选择。请重试。"}))


def confirm_start() -> bool:
    choice = input(t({"en": "Start the tower run? [Y/n]: ", "zh": "开始塔楼冒险？[Y/n]："})).strip().lower()
    return choice in {"", "y", "yes"}


def prompt_item_use(player) -> str:
    if not player.inventory:
        print(f"\n{t({'en': 'HP', 'zh': '生命值'})}: {player.hp}/{player.total_max_hp}")
        choice = input(t({"en": "Press Enter to continue, 's' to save, or 'a' for achievements: ", "zh": "按回车继续、输入's'保存或输入'a'查看成就："})).strip()
        return choice
    print(f"\n{t({'en': 'HP', 'zh': '生命值'})}: {player.hp}/{player.total_max_hp}")
    render_inventory(player)
    choice = input(t({"en": "Use item (u<number>), Equip (e<number>), 's' to save, 'a' for achievements, or Enter to continue: ", "zh": "使用物品（u数字）、装备（e数字）、输入's'保存、输入'a'查看成就或回车继续："})).strip()
    return choice


def prompt_event_choice(event) -> int:
    """Prompt player to choose an event option.

    Returns:
        Index of the chosen option (0-based)
    """
    print(f"\n=== {event.get_name()} ===")
    print(event.get_description())
    print()
    for i, choice in enumerate(event.choices, 1):
        print(f"{i}. {choice.get_text()}")
    print()

    while True:
        choice = input(t({"en": "Choose an option: ", "zh": "选择一个选项："})).strip()
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(event.choices):
                return idx
        print(t({"en": "Invalid choice. Try again.", "zh": "无效的选择。请重试。"}))


def prompt_shop_purchase(shop, player, items_db) -> tuple[int, bool]:
    """Prompt player to purchase from shop.

    Returns:
        (item_index, should_leave) - item_index is -1 if no purchase, should_leave indicates if player wants to exit shop
    """
    print(f"\n=== {shop.get_name()} ===")
    print(shop.get_description())
    print(f"{t({'en': 'Your gold', 'zh': '你的金币'})}: {player.gold}")
    print()

    for i, shop_item in enumerate(shop.items, 1):
        if shop_item.is_available():
            item = items_db.get(shop_item.item_name)
            if item:
                stock_text = ""
                if shop_item.stock > 0:
                    stock_text = f" ({t({'en': 'stock', 'zh': '库存'})}: {shop_item.stock})"
                print(f"{i}. {item.get_name()} - {shop_item.price} {t({'en': 'gold', 'zh': '金币'})}{stock_text}")
                print(f"   {item.get_description()}")

    print()
    choice = input(t({"en": "Buy item (number) or Enter to leave: ", "zh": "购买物品（数字）或回车离开："})).strip()

    if not choice:
        return -1, True

    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(shop.items):
            return idx, False

    print(t({"en": "Invalid choice.", "zh": "无效的选择。"}))
    return -1, False
