from game.game_state import GameState
from game.i18n import t
from cli.colors import Color, colorize, hp_color, mp_color, rarity_color


def render_intro() -> None:
    title = t({"en": "== Tower Prototype ==", "zh": "== 塔楼原型 =="})
    print(colorize(title, Color.BRIGHT_CYAN))
    print(t({"en": "A minimal CLI roguelike built for AI-driven iterative development.", "zh": "一个为AI驱动的迭代开发而构建的最小CLI Roguelike游戏。"}))


def render_inventory(player) -> None:
    print(colorize(t({"en": "Equipment:", "zh": "装备："}), Color.BOLD))
    weapon_name = _format_item_with_rarity(player.weapon) if player.weapon else colorize(t({"en": "(none)", "zh": "（无）"}), Color.GRAY)
    armor_name = _format_item_with_rarity(player.armor) if player.armor else colorize(t({"en": "(none)", "zh": "（无）"}), Color.GRAY)
    accessory_name = _format_item_with_rarity(player.accessory) if player.accessory else colorize(t({"en": "(none)", "zh": "（无）"}), Color.GRAY)
    print(f"  {colorize(t({'en': 'Weapon', 'zh': '武器'}), Color.YELLOW)}: {weapon_name}")
    print(f"  {colorize(t({'en': 'Armor', 'zh': '护甲'}), Color.CYAN)}: {armor_name}")
    print(f"  {colorize(t({'en': 'Accessory', 'zh': '饰品'}), Color.MAGENTA)}: {accessory_name}")

    if not player.inventory:
        print(colorize(t({"en": "Inventory: (empty)", "zh": "背包：（空）"}), Color.GRAY))
        return
    print(colorize(t({"en": "Inventory:", "zh": "背包："}), Color.BOLD))
    for i, item in enumerate(player.inventory):
        item_display = _format_item_with_rarity(item)
        print(f"  {i+1}. {item_display} - {item.get_description()}")


def _format_item_with_rarity(item) -> str:
    """Format item name with rarity indicator and color."""
    name = item.get_name()
    rarity = getattr(item, 'rarity', 'common')
    color = rarity_color(rarity)

    if rarity == 'rare':
        return colorize(f"[★] {name}", color)
    elif rarity == 'epic':
        return colorize(f"[★★] {name}", color)
    elif rarity == 'legendary':
        return colorize(f"[★★★] {name}", color)
    return colorize(name, color)


def render_state(state: GameState) -> None:
    print()
    print(colorize(t({"en": "== Final Summary ==", "zh": "== 最终总结 =="}), Color.BRIGHT_CYAN))

    # Player info with colors
    hp_col = hp_color(state.player.hp, state.player.total_max_hp)
    print(
        f"{colorize(state.player.name, Color.BRIGHT_YELLOW)} | "
        f"{t({'en': 'Level', 'zh': '等级'})} {colorize(str(state.player.level), Color.GREEN)} | "
        f"{t({'en': 'HP', 'zh': '生命值'})} {colorize(f'{state.player.hp}/{state.player.total_max_hp}', hp_col)} | "
        f"{t({'en': 'Gold', 'zh': '金币'})} {colorize(str(state.player.gold), Color.YELLOW)}"
    )
    print(
        f"{t({'en': 'Attack', 'zh': '攻击力'})}: {colorize(str(state.player.total_attack), Color.RED)} | "
        f"{t({'en': 'Defense', 'zh': '防御力'})}: {colorize(str(state.player.total_defense), Color.CYAN)}"
    )
    print(t({"en": f"Reached floor: {state.floor}", "zh": f"到达楼层：{state.floor}"}))
    render_inventory(state.player)
    print()
    print(colorize(t({"en": "== Run Log ==", "zh": "== 运行日志 =="}), Color.BRIGHT_CYAN))
    for entry in state.log:
        print(f"- {entry}")
