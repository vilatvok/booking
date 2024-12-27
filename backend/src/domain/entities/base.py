from dataclasses import dataclass, asdict


@dataclass
class Entity:
    id: int

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def to_dict(self):
        return asdict(self)