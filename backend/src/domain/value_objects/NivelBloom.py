from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class NivelBloom:
    nivel: int
    nombre: str
    nivel_legado: str
    descripcion: str
    verbos: List[str] = field(default_factory=list)
