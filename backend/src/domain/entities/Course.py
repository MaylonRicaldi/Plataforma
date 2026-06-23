from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Course:
    id: str
    name: str
    description: Optional[str] = None
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None

    def to_dict(self) -> dict:
        return {k: v for k, v in asdict(self).items() if v is not None}
