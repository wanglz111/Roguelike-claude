from game.game_state import GameState
from game.i18n import t


def render_intro() -> None:
    print(t({"en": "== Tower Prototype ==", "zh": "== 塔楼原型 =="}))
    print(t({"en": "A minimal CLI roguelike built for AI-driven iterative development.", "zh": "一个为AI驱动的迭代开发而构建的最小CLI Roguelike游戏。"}))


def render_inventory(player) -> None:
    print(t({"en": "Equipment:", "zh": "装备："}))
    weapon_name = player.weapon.get_name() if player.weapon else t({"en": "(none)", "zh": "（无）"})
    armor_name = player.armor.get_name() if player.armor else t({"en": "(none)", "zh": "（无）"})
    accessory_name = player.accessory.get_name() if player.accessory else t({"en": "(none)", "zh": "（无）"})
    print(f"  {t({'en': 'Weapon', 'zh': '武器'})}: {weapon_name}")
    print(f"  {t({'en': 'Armor', 'zh': '护甲'})}: {armor_name}")
    print(f"  {t({'en': 'Accessory', 'zh': '饰品'})}: {accessory_name}")

    if not player.inventory:
        print(t({"en": "Inventory: (empty)", "zh": "背包：（空）"}))
        return
    print(t({"en": "Inventory:", "zh": "背包："}))
    for i, item in enumerate(player.inventory):
        print(f"  {i+1}. {item.get_name()} - {item.get_description()}")


def render_state(state: GameState) -> None:
    print()
    print(t({"en": "== Final Summary ==", "zh": "== 最终总结 =="}))
    print(
        f"{state.player.name} | {t({'en': 'Level', 'zh': '等级'})} {state.player.level} | "
        f"{t({'en': 'HP', 'zh': '生命值'})} {state.player.hp}/{state.player.total_max_hp} | {t({'en': 'Gold', 'zh': '金币'})} {state.player.gold}"
    )
    print(f"{t({'en': 'Attack', 'zh': '攻击力'})}: {state.player.total_attack} | {t({'en': 'Defense', 'zh': '防御力'})}: {state.player.total_defense}")
    print(t({"en": f"Reached floor: {state.floor}", "zh": f"到达楼层：{state.floor}"}))
    render_inventory(state.player)
    print()
    print(t({"en": "== Run Log ==", "zh": "== 运行日志 =="}))
    for entry in state.log:
        print(f"- {entry}")
