from game.monster import Monster
from game.player import Player
from game.i18n import t


def calculate_damage(attack: int, defense: int) -> int:
    return max(1, attack - defense)


def fight(player: Player, monster: Monster) -> tuple[bool, list[str]]:
    monster_name = monster.get_name()
    log = [t({"en": f"A wild {monster_name} appears!", "zh": f"一只野生的{monster_name}出现了！"})]
    round_number = 1

    while player.is_alive and monster.hp > 0:
        player_damage = calculate_damage(player.attack, monster.defense)
        monster.hp -= player_damage
        log.append(
            t({"en": f"Round {round_number}: You hit {monster_name} for {player_damage} damage.", "zh": f"第{round_number}回合：你对{monster_name}造成了{player_damage}点伤害。"})
        )
        if monster.hp <= 0:
            break

        monster_damage = calculate_damage(monster.attack, player.defense)
        player.hp -= monster_damage
        log.append(t({"en": f"{monster_name} hits you for {monster_damage} damage.", "zh": f"{monster_name}对你造成了{monster_damage}点伤害。"}))
        round_number += 1

    if player.is_alive:
        log.append(t({"en": f"You defeated {monster_name}.", "zh": f"你击败了{monster_name}。"}))
        log.extend(player.gain_rewards(monster.exp_reward, monster.gold_reward))
        return True, log

    player.hp = 0
    log.append(t({"en": "You were defeated.", "zh": "你被击败了。"}))
    return False, log
