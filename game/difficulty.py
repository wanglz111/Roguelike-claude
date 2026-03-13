from enum import Enum


class Difficulty(Enum):
    EASY = "easy"
    NORMAL = "normal"
    HARD = "hard"

    def get_monster_hp_mult(self) -> float:
        return {
            Difficulty.EASY: 0.7,
            Difficulty.NORMAL: 1.0,
            Difficulty.HARD: 1.4
        }[self]

    def get_monster_attack_mult(self) -> float:
        return {
            Difficulty.EASY: 0.8,
            Difficulty.NORMAL: 1.0,
            Difficulty.HARD: 1.3
        }[self]

    def get_gold_mult(self) -> float:
        return {
            Difficulty.EASY: 1.2,
            Difficulty.NORMAL: 1.0,
            Difficulty.HARD: 0.8
        }[self]

    def get_drop_rate_mult(self) -> float:
        return {
            Difficulty.EASY: 1.3,
            Difficulty.NORMAL: 1.0,
            Difficulty.HARD: 0.7
        }[self]
