from dataclasses import dataclass
from typing import Union, Dict, List

from game.i18n import t


@dataclass
class EventChoice:
    """A choice the player can make in an event."""
    text: Union[str, Dict[str, str]]
    effect_type: str  # "heal", "damage", "gold", "nothing"
    effect_value: int
    result_text: Union[str, Dict[str, str]]

    def get_text(self) -> str:
        """Get localized choice text."""
        return t(self.text)

    def get_result_text(self) -> str:
        """Get localized result text."""
        return t(self.result_text)


@dataclass
class Event:
    """A random event that can occur between floors."""
    name: Union[str, Dict[str, str]]
    description: Union[str, Dict[str, str]]
    choices: List[EventChoice]
    min_floor: int = 1

    def get_name(self) -> str:
        """Get localized name."""
        return t(self.name)

    def get_description(self) -> str:
        """Get localized description."""
        return t(self.description)
