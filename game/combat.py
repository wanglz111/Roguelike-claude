import random

from game.monster import Monster
from game.player import Player
from game.skill import Skill
from game.i18n import t
from game.status_effect import load_status_effects, ActiveStatusEffect

# Load status effects once at module level
_status_effects_db = None


def get_status_effects_db():
    global _status_effects_db
    if _status_effects_db is None:
        _status_effects_db = load_status_effects()
    return _status_effects_db


def calculate_damage(attack: int, defense: int, is_critical: bool = False) -> int:
    base_damage = max(1, attack - defense)
    if is_critical:
        return base_damage * 2
    return base_damage


def check_critical_hit(crit_chance: float = 0.1) -> bool:
    """Check if an attack is a critical hit. Default 10% chance."""
    return random.random() < crit_chance


def fight(player: Player, monster: Monster, skill: Skill = None) -> tuple[bool, list[str]]:
    monster_name = monster.get_name()
    if monster.is_boss:
        log = [
            "═" * 50,
            t({"en": f"⚔️ BOSS BATTLE! {monster_name} appears!", "zh": f"⚔️ Boss战！{monster_name}出现了！"}),
            t({"en": f"HP: {monster.hp} | ATK: {monster.attack} | DEF: {monster.defense}", "zh": f"生命值：{monster.hp} | 攻击：{monster.attack} | 防御：{monster.defense}"}),
            "═" * 50
        ]
    else:
        log = [t({"en": f"⚔️ A wild {monster_name} appears!", "zh": f"⚔️ 一只野生的{monster_name}出现了！"})]
    round_number = 1
    defense_boost = 0.0

    while player.is_alive and monster.hp > 0:
        # Process status effects at the start of each round (after round 1)
        if round_number > 1:
            status_messages = player.process_status_effects()
            log.extend(status_messages)

            # Check if player died from status effects
            if not player.is_alive:
                break

        # Player's turn
        if skill and round_number == 1:
            # Use skill on first round
            if skill.effect_type == "damage_multiplier":
                player_crit = check_critical_hit()
                player_damage = int(calculate_damage(player.total_attack, monster.defense, player_crit) * skill.effect_value)
                monster.hp -= player_damage
                log.append(t({"en": f"Round {round_number}: You use {skill.get_name()}! {player_damage} damage to {monster_name}.",
                             "zh": f"第{round_number}回合：你使用了{skill.get_name()}！对{monster_name}造成{player_damage}点伤害。"}))
            elif skill.effect_type == "heal":
                old_hp = player.hp
                player.hp = min(player.hp + int(skill.effect_value), player.total_max_hp)
                healed = player.hp - old_hp
                log.append(t({"en": f"Round {round_number}: You use {skill.get_name()}! Restored {healed} HP.",
                             "zh": f"第{round_number}回合：你使用了{skill.get_name()}！恢复了{healed}点生命值。"}))
            elif skill.effect_type == "defense_boost":
                defense_boost = skill.effect_value
                log.append(t({"en": f"Round {round_number}: You use {skill.get_name()}! Defense increased.",
                             "zh": f"第{round_number}回合：你使用了{skill.get_name()}！防御力提升。"}))
            elif skill.effect_type == "vampiric":
                player_crit = check_critical_hit()
                player_damage = int(calculate_damage(player.total_attack, monster.defense, player_crit) * skill.effect_value)
                monster.hp -= player_damage
                old_hp = player.hp
                heal_amount = getattr(skill, 'heal_amount', 10)
                player.hp = min(player.hp + heal_amount, player.total_max_hp)
                healed = player.hp - old_hp
                log.append(t({"en": f"Round {round_number}: You use {skill.get_name()}! {player_damage} damage to {monster_name}, restored {healed} HP.",
                             "zh": f"第{round_number}回合：你使用了{skill.get_name()}！对{monster_name}造成{player_damage}点伤害，恢复了{healed}点生命值。"}))

            # Apply status effect if skill has one
            if skill.status_effect_id:
                status_db = get_status_effects_db()
                if skill.status_effect_id in status_db:
                    status_effect = status_db[skill.status_effect_id]
                    active_effect = ActiveStatusEffect(
                        effect=status_effect,
                        remaining_turns=status_effect.duration
                    )
                    status_msg = player.add_status_effect(active_effect)
                    log.append(status_msg)
        else:
            # Normal attack
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
        if defense_boost > 0:
            monster_damage = int(monster_damage * (1 - defense_boost))
            defense_boost = 0.0
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
        log.append("─" * 50)
        log.append(t({"en": f"✓ Victory! You defeated {monster_name}.", "zh": f"✓ 胜利！你击败了{monster_name}。"}))
        log.extend(player.gain_rewards(monster.exp_reward, monster.gold_reward))
        return True, log

    player.hp = 0
    log.append("─" * 50)
    log.append(t({"en": "✗ Defeat! You were defeated.", "zh": "✗ 失败！你被击败了。"}))
    return False, log
