from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class Question:
    courseId: str
    courseName: str
    userId: str
    userName: str
    questionText: str
    aiLevel: str = "bajo"
    aiFeedback: str = ""
    improvedQuestion: str = ""
    bloomLevel: Optional[int] = None
    bloomNombre: Optional[str] = None
    cursoDetectado: Optional[str] = None
    idempotencyKey: Optional[str] = None
    id: Optional[str] = None
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None

    def to_dict(self) -> dict:
        return {k: v for k, v in asdict(self).items() if v is not None}
