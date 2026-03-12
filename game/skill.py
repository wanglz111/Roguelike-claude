import json
from dataclasses import dataclass
from game.i18n import t


@dataclass
class Skill:
    skill_id: str
    name: dict
    description: dict
    mp_cost: int
    effect_type: str
    effect_value: float

    def get_name(self) -> str:
        return t(self.name)

    def get_description(self) -> str:
        return t(self.description)


def load_skills() -> dict[str, Skill]:
    with open("content/skills.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return {
        skill_id: Skill(
            skill_id=skill_id,
            name=skill_data["name"],
            description=skill_data["description"],
            mp_cost=skill_data["mp_cost"],
            effect_type=skill_data["effect_type"],
            effect_value=skill_data["effect_value"],
        )
        for skill_id, skill_data in data.items()
    }
