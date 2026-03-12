from dataclasses import dataclass, field

from game.player import Player


@dataclass
class GameState:
    player: Player
    floor: int = 1
    max_floor: int = 5
    game_over: bool = False
    log: list[str] = field(default_factory=list)
    cycle: int = 1
