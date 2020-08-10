from enum import Enum


class AbilityKind(Enum):
    PASSIVE = 0
    Q = 1
    W = 2
    E = 3
    R = 4


class Ability:
    def __init__(self, kind, name, description, cooldown):
        self.name = name
        self.description = description
        self.cooldown = cooldown
        self.kind = kind

    @classmethod
    def fromJson(cls, json, kind):
        name = json['name']
        description = json['description']
        cooldown = json.get['cooldownBurn']
        kind = kind
        return cls(name, kind, description, cooldown)


