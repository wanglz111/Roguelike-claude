from dataclasses import dataclass


@dataclass
class Monster:
    name: str
    hp: int
    attack: int
    defense: int
    exp_reward: int
    gold_reward: int
