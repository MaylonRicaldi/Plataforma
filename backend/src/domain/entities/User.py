from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class User:
    uid: str
    email: str
    name: str
    role: str = "student"
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None

    def to_dict(self) -> dict:
        return {k: v for k, v in asdict(self).items() if v is not None}
