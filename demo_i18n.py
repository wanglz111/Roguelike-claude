#!/usr/bin/env python3
"""Demo script to showcase bilingual support."""

from game.engine import run_game
from game.game_state import GameState
from game.player import Player
from game.i18n import get_i18n


def demo_language(lang: str, player_name: str):
    """Run a short game demo in the specified language."""
    get_i18n().set_language(lang)

    lang_name = "English" if lang == "en" else "中文"
    print(f"\n{'='*60}")
    print(f"Demo in {lang_name}")
    print('='*60)

    state = GameState(player=Player(name=player_name))
    state.max_floor = 2  # Short demo

    result = run_game(state, seed=42)

    print(f"\n{'='*60}")
    print("Game Log / 游戏日志:")
    print('='*60)
    for entry in result.log:
        print(f"  {entry}")

    print(f"\n{'='*60}")
    print(f"Final Status / 最终状态:")
    print('='*60)
    print(f"  Player: {result.player.name}")
    print(f"  Level: {result.player.level}")
    print(f"  HP: {result.player.hp}/{result.player.max_hp}")
    print(f"  Gold: {result.player.gold}")
    print(f"  Floor: {result.floor}")
    print(f"  Victory: {result.player.is_alive}")


if __name__ == "__main__":
    print("Roguelike Bilingual Demo")
    print("=" * 60)

    # Demo in English
    demo_language("en", "Hero")

    # Demo in Chinese
    demo_language("zh", "英雄")

    print("\n" + "="*60)
    print("Demo completed! / 演示完成！")
    print("="*60)
