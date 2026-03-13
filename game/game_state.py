from dataclasses import dataclass, field

from game.player import Player
from game.difficulty import Difficulty


@dataclass
class GameState:
    player: Player
    floor: int = 1
    max_floor: int = 5
    game_over: bool = False
    log: list[str] = field(default_factory=list)
    cycle: int = 1
    difficulty: Difficulty = Difficulty.NORMAL
