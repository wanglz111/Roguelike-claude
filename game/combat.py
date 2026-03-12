import random

from game.monster import Monster
from game.player import Player
from game.i18n import t


def calculate_damage(attack: int, defense: int, is_critical: bool = False) -> int:
    base_damage = max(1, attack - defense)
    if is_critical:
        return base_damage * 2
    return base_damage


def check_critical_hit(crit_chance: float = 0.1) -> bool:
    """Check if an attack is a critical hit. Default 10% chance."""
    return random.random() < crit_chance


def fight(player: Player, monster: Monster) -> tuple[bool, list[str]]:
    monster_name = monster.get_name()
    if monster.is_boss:
        log = [t({"en": f"⚔️ BOSS BATTLE! {monster_name} appears!", "zh": f"⚔️ Boss战！{monster_name}出现了！"})]
    else:
        log = [t({"en": f"A wild {monster_name} appears!", "zh": f"一只野生的{monster_name}出现了！"})]
    round_number = 1

    while player.is_alive and monster.hp > 0:
        # Player's turn
        player_crit = check_critical_hit()
        player_damage = calculate_damage(player.total_attack, monster.defense, player_crit)
        monster.hp -= player_damage

        if player_crit:
            log.append(
                t({"en": f"Round {round_number}: Critical hit! You hit {monster_name} for {player_damage} damage.",
                   "zh": f"第{round_number}回合：暴击！你对{monster_name}造成了{player_damage}点伤害。"})
            )
        else:
            log.append(
                t({"en": f"Round {round_number}: You hit {monster_name} for {player_damage} damage.",
                   "zh": f"第{round_number}回合：你对{monster_name}造成了{player_damage}点伤害。"})
            )

        if monster.hp <= 0:
            break

        # Monster's turn
        monster_crit = check_critical_hit()
        monster_damage = calculate_damage(monster.attack, player.total_defense, monster_crit)
        player.hp -= monster_damage

        if monster_crit:
            log.append(
                t({"en": f"{monster_name} lands a critical hit on you for {monster_damage} damage!",
                   "zh": f"{monster_name}对你造成了暴击，{monster_damage}点伤害！"})
            )
        else:
            log.append(
                t({"en": f"{monster_name} hits you for {monster_damage} damage.",
                   "zh": f"{monster_name}对你造成了{monster_damage}点伤害。"})
            )

        round_number += 1

    if player.is_alive:
        log.append(t({"en": f"You defeated {monster_name}.", "zh": f"你击败了{monster_name}。"}))
        log.extend(player.gain_rewards(monster.exp_reward, monster.gold_reward))
        return True, log

    player.hp = 0
    log.append(t({"en": "You were defeated.", "zh": "你被击败了。"}))
    return False, log
