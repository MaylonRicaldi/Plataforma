import logging

from src.infrastructure.adapters.outbound.ai.bloom_data import (
    NIVELES_BLOOM, RECOMENDACIONES_BLOOM, MEJORAS_BLOOM,
)
from src.infrastructure.adapters.outbound.ai.text_utils import (
    quitar_acentos, lematizar, extraer_tema,
)
from src.infrastructure.adapters.outbound.ai.course_detector import (
    detectar_curso, NOMBRES_CURSOS,
)

logger = logging.getLogger(__name__)

_NIVELES_NORM = {
    nivel: [quitar_acentos(v) for v in info["verbos"]]
    for nivel, info in NIVELES_BLOOM.items()
}

_NIVELES_LEMMA = {
    nivel: [quitar_acentos(lematizar(v)) for v in info["verbos"]]
    for nivel, info in NIVELES_BLOOM.items()
}


def clasificar_nivel_bloom(pregunta: str) -> int:
    p_norm = quitar_acentos(pregunta)
    p_lemma = lematizar(pregunta)

    for nivel in sorted(NIVELES_BLOOM.keys(), reverse=True):
        if any(v in p_norm for v in _NIVELES_NORM[nivel]):
            return nivel
        if any(v in p_lemma for v in _NIVELES_LEMMA[nivel]):
            return nivel

    p_lower = pregunta.lower().strip()
    if p_lower.startswith("qué opinas") or p_lower.startswith("estás de acuerdo"):
        return 4
    if p_lower.startswith("qué pasaría si") or p_lower.startswith("cómo solucionarías"):
        return 5
    if p_lower.startswith("por qué") or p_lower.startswith("cuál es la relación"):
        return 3
    if p_lower.startswith("cómo"):
        return 2
    if p_lower.startswith("qué es") or p_lower.startswith("cuál es") or p_lower.startswith("quién fue"):
        return 0

    return 1


def construir_feedback(nivel_idx: int, curso: str | None) -> str:
    info       = NIVELES_BLOOM[nivel_idx]
    nivel_num  = nivel_idx + 1
    nombre     = info["nombre"]
    descripcion = info["descripcion"]
    rec        = RECOMENDACIONES_BLOOM[nivel_idx]
    curso_txt  = f" | Curso: {NOMBRES_CURSOS.get(curso, curso)}" if curso else ""
    return f"Nivel {nivel_num}/6 — {nombre}{curso_txt}. {descripcion} {rec}"


def bloom_engine(question_text: str) -> dict:
    nivel_idx = clasificar_nivel_bloom(question_text)
    curso     = detectar_curso(question_text)
    info      = NIVELES_BLOOM[nivel_idx]
    tema      = extraer_tema(question_text)

    return {
        "level":             info["nivel_legado"],
        "bloom_level":       nivel_idx + 1,
        "bloom_nombre":      info["nombre"],
        "curso_detectado":   curso,
        "feedback":          construir_feedback(nivel_idx, curso),
        "improved_question": MEJORAS_BLOOM[nivel_idx](tema),
    }
