from src.infrastructure.adapters.outbound.ai.text_utils import quitar_acentos

CURSOS_KEYWORDS = {
    "matematica": [
        "número", "fracción", "ecuación", "álgebra", "geometría", "triángulo",
        "ángulo", "área", "perímetro", "volumen", "porcentaje", "razón",
        "proporción", "función", "gráfica", "estadística", "probabilidad",
        "entero", "decimal", "mcd", "mcm", "potencia", "raíz", "expresión",
        "variable", "incógnita", "polinomio", "conjunto", "operación",
    ],
    "geografia": [
        "relieve", "clima", "región", "bioma", "río", "océano", "continente",
        "país", "capital", "mapa", "latitud", "longitud", "población",
        "migración", "recurso natural", "medio ambiente", "ecosistema",
        "sierra", "selva", "costa", "perú", "amazonia", "andes", "territorio",
        "suelo", "hidrografía", "cuenca", "demografía", "urbanización",
    ],
    "ciencia_tecnologia": [
        "célula", "átomo", "molécula", "energía", "fuerza", "materia",
        "reacción", "elemento", "compuesto", "mezcla", "luz", "sonido",
        "electricidad", "magnetismo", "ecosistema", "biodiversidad",
        "organismo", "evolución", "genética", "salud", "tecnología", "circuito",
        "fotosíntesis", "respiración", "química", "física", "biología", "newton",
    ],
    "educacion_civica": [
        "derecho", "deber", "ciudadano", "estado", "gobierno", "democracia",
        "constitución", "ley", "norma", "participación", "identidad",
        "cultura", "diversidad", "ética", "valores", "familia", "sociedad",
        "institución", "poder", "elección", "voto", "libertad", "igualdad",
        "justicia", "responsabilidad", "comunidad", "convivencia", "civismo",
    ],
    "comunicacion": [
        "texto", "párrafo", "oración", "narración", "descripción", "argumento",
        "personaje", "autor", "obra", "género", "literatura", "poesía",
        "cuento", "novela", "ortografía", "gramática", "comprensión lectora",
        "idea principal", "coherencia", "cohesión", "comunicación", "lenguaje",
        "redacción", "ensayo", "diálogo", "sinónimo", "antónimo", "metáfora",
    ],
    "ingles": [
        "verb", "noun", "adjective", "sentence", "grammar", "vocabulary",
        "tense", "present", "past", "future", "reading", "writing",
        "listening", "speaking", "word", "phrase", "translation", "meaning",
        "dialogue", "expression", "pronoun", "preposition", "question",
        "singular", "plural", "adverb", "conditional", "modal",
    ],
    "computacion": [
        "computadora", "software", "hardware", "programa", "algoritmo",
        "internet", "red", "dato", "archivo", "sistema operativo",
        "procesador", "memoria", "base de datos", "código", "aplicación",
        "dispositivo", "tecnología", "digital", "ciberseguridad", "navegador",
        "hoja de cálculo", "presentación", "celda", "fórmula", "variable",
    ],
    "historia": [
        "civilización", "cultura", "período", "época", "guerra", "revolución",
        "imperio", "colonia", "independencia", "presidente", "gobierno",
        "economía", "sociedad", "conquista", "virreinato", "república",
        "prehistoria", "cronología", "fuente histórica", "perú", "incas",
        "españa", "coloniaje", "emancipación", "caudillo", "conflicto",
    ],
}

NOMBRES_CURSOS = {
    "matematica":        "Matemática",
    "geografia":         "Geografía",
    "ciencia_tecnologia":"Ciencia y Tecnología",
    "educacion_civica":  "Educación Cívica",
    "comunicacion":      "Comunicación",
    "ingles":            "Inglés",
    "computacion":       "Computación",
    "historia":          "Historia",
}

_CURSOS_NORM = {
    curso: [quitar_acentos(kw) for kw in kws]
    for curso, kws in CURSOS_KEYWORDS.items()
}


def detectar_curso(pregunta: str) -> str | None:
    p_norm = quitar_acentos(pregunta)

    hits = {}
    for curso, kws_norm in _CURSOS_NORM.items():
        count = sum(1 for kw in kws_norm if kw in p_norm)
        if count > 0:
            hits[curso] = count

    return max(hits, key=hits.get) if hits else None
