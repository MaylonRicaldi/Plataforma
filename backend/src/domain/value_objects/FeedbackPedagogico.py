from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class FeedbackPedagogico:
    texto: str
    recomendacion: Optional[str] = None
    mejora_template: Optional[str] = None
