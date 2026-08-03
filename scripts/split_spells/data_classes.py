from dataclasses import dataclass

@dataclass
class Spell:
    name:    str
    content: list[str]

# TODO: add convenience features
@dataclass
class SpellBook:
    spells: dict[str, Spell]

PATTERN_LIST = [
    "Blinded",
    "Charmed",
    "Deafened",
    "Exhaustion",
    "Frightened",
    "Grappled",
    "Incapacitated",
    "Invisible",
    "Paralyzed",
    "Petrified",
    "Poisoned",
    "Prone",
    "Restrained",
    "Stunned",
    "Unconscious",
]
