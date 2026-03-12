from game.monster import Monster
from game.player import Player


def calculate_damage(attack: int, defense: int) -> int:
    return max(1, attack - defense)


def fight(player: Player, monster: Monster) -> tuple[bool, list[str]]:
    log = [f"A wild {monster.name} appears!"]
    round_number = 1

    while player.is_alive and monster.hp > 0:
        player_damage = calculate_damage(player.attack, monster.defense)
        monster.hp -= player_damage
        log.append(
            f"Round {round_number}: You hit {monster.name} for {player_damage} damage."
        )
        if monster.hp <= 0:
            break

        monster_damage = calculate_damage(monster.attack, player.defense)
        player.hp -= monster_damage
        log.append(f"{monster.name} hits you for {monster_damage} damage.")
        round_number += 1

    if player.is_alive:
        log.append(f"You defeated {monster.name}.")
        log.extend(player.gain_rewards(monster.exp_reward, monster.gold_reward))
        return True, log

    player.hp = 0
    log.append("You were defeated.")
    return False, log
