import os
import json
import logging

from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()


# ============================================================
# TAXONOMÍA DE BLOOM — CONTEXTUALIZADA PARA 2DO DE SECUNDARIA
# ============================================================

NIVELES_BLOOM = {
    0: {
        "nombre": "Recordar",
        "nivel_legado": "bajo",
        "descripcion": "El estudiante recupera información básica de memoria.",
        "verbos": [
            "qué es", "define", "definir", "qué son", "cuál es", "cuáles son",
            "menciona", "mencionar", "lista", "listar", "nombra", "nombrar",
            "identifica", "identificar", "enuncia", "enunciar", "reconoce",
            "señala", "señalar", "escribe", "cuándo", "dónde ocurrió",
            "quién fue", "qué significa"
        ]
    },
    1: {
        "nombre": "Comprender",
        "nivel_legado": "bajo",
        "descripcion": "El estudiante demuestra que entiende el concepto con sus propias palabras.",
        "verbos": [
            "explica", "explicar", "describe", "describir", "resume", "resumir",
            "cómo funciona", "cómo se produce", "cómo ocurre", "interpreta",
            "interpretar", "clasifica", "clasificar", "parafrasea", "ilustra",
            "relaciona", "relata", "por qué ocurre", "en qué consiste",
            "qué entiendes", "qué significa para ti"
        ]
    },
    2: {
        "nombre": "Aplicar",
        "nivel_legado": "medio",
        "descripcion": "El estudiante usa lo aprendido para resolver una situación concreta.",
        "verbos": [
            "aplica", "aplicar", "usa", "utiliza", "utilizar", "resuelve",
            "resolver", "implementa", "demuestra", "calcula", "calcular",
            "ejecuta", "construye", "desarrolla", "emplea", "practica",
            "realiza", "efectúa", "opera", "si tuvieras que", "cómo usarías",
            "en qué caso", "cómo resolverías", "cómo aplicarías"
        ]
    },
    3: {
        "nombre": "Analizar",
        "nivel_legado": "medio",
        "descripcion": "El estudiante descompone información y examina sus partes y relaciones.",
        "verbos": [
            "analiza", "analizar", "compara", "comparar", "diferencia",
            "diferenciar", "examina", "examinar", "descompone", "distingue",
            "distinguir", "organiza", "organizar", "contrasta", "contrastar",
            "estructura", "por qué crees", "qué relación existe",
            "en qué se parecen", "en qué se diferencian", "qué factores",
            "qué causas", "qué consecuencias", "cómo se relaciona"
        ]
    },
    4: {
        "nombre": "Evaluar",
        "nivel_legado": "alto",
        "descripcion": "El estudiante emite un juicio razonado usando criterios.",
        "verbos": [
            "evalúa", "evaluar", "critica", "criticar", "justifica",
            "justificar", "argumenta", "argumentar", "valora", "valorar",
            "defiende", "defender", "juzga", "recomienda", "recomendar",
            "prioriza", "fundamenta", "opina", "qué opinas", "estás de acuerdo",
            "consideras que", "por qué es importante", "qué tan válido",
            "cuál sería mejor", "cómo mejorarías", "qué tan correcto"
        ]
    },
    5: {
        "nombre": "Crear",
        "nivel_legado": "alto",
        "descripcion": "El estudiante produce algo nuevo combinando lo aprendido.",
        "verbos": [
            "diseña", "diseñar", "crea", "crear", "propone", "proponer",
            "formula", "formular", "planifica", "planificar", "genera",
            "elabora", "elaborar", "inventa", "inventar", "desarrolla un",
            "construye un", "escribe un", "redacta", "produce", "imagina",
            "cómo crearías", "qué propondrías", "si pudieras diseñar"
        ]
    }
}

# ============================================================
# VOCABULARIO ESPECÍFICO POR CURSO (2DO SECUNDARIA — PERÚ)
# ============================================================

CURSOS_KEYWORDS = {
    "matematica": [
        "número", "fracción", "ecuación", "álgebra", "geometría", "triángulo",
        "ángulo", "área", "perímetro", "volumen", "porcentaje", "razón",
        "proporción", "función", "gráfica", "estadística", "probabilidad",
        "entero", "decimal", "mcd", "mcm", "potencia", "raíz", "expresión",
        "variable", "incógnita", "polinomio", "conjunto", "operación"
    ],
    "geografia": [
        "relieve", "clima", "región", "bioma", "río", "océano", "continente",
        "país", "capital", "mapa", "latitud", "longitud", "población",
        "migración", "recurso natural", "medio ambiente", "ecosistema",
        "sierra", "selva", "costa", "perú", "amazonia", "andes", "territorio",
        "suelo", "hidrografía", "cuenca", "demografía", "urbanización"
    ],
    "ciencia_tecnologia": [
        "célula", "átomo", "molécula", "energía", "fuerza", "materia",
        "reacción", "elemento", "compuesto", "mezcla", "luz", "sonido",
        "electricidad", "magnetismo", "ecosistema", "biodiversidad",
        "organismo", "evolución", "genética", "salud", "tecnología", "circuito",
        "fotosíntesis", "respiración", "química", "física", "biología", "newton"
    ],
    "educacion_civica": [
        "derecho", "deber", "ciudadano", "estado", "gobierno", "democracia",
        "constitución", "ley", "norma", "participación", "identidad",
        "cultura", "diversidad", "ética", "valores", "familia", "sociedad",
        "institución", "poder", "elección", "voto", "libertad", "igualdad",
        "justicia", "responsabilidad", "comunidad", "convivencia", "civismo"
    ],
    "comunicacion": [
        "texto", "párrafo", "oración", "narración", "descripción", "argumento",
        "personaje", "autor", "obra", "género", "literatura", "poesía",
        "cuento", "novela", "ortografía", "gramática", "comprensión lectora",
        "idea principal", "coherencia", "cohesión", "comunicación", "lenguaje",
        "redacción", "ensayo", "diálogo", "sinónimo", "antónimo", "metáfora"
    ],
    "ingles": [
        "verb", "noun", "adjective", "sentence", "grammar", "vocabulary",
        "tense", "present", "past", "future", "reading", "writing",
        "listening", "speaking", "word", "phrase", "translation", "meaning",
        "dialogue", "expression", "pronoun", "preposition", "question",
        "singular", "plural", "adverb", "conditional", "modal"
    ],
    "computacion": [
        "computadora", "software", "hardware", "programa", "algoritmo",
        "internet", "red", "dato", "archivo", "sistema operativo",
        "procesador", "memoria", "base de datos", "código", "aplicación",
        "dispositivo", "tecnología", "digital", "ciberseguridad", "navegador",
        "hoja de cálculo", "presentación", "celda", "fórmula", "variable"
    ],
    "historia": [
        "civilización", "cultura", "período", "época", "guerra", "revolución",
        "imperio", "colonia", "independencia", "presidente", "gobierno",
        "economía", "sociedad", "conquista", "virreinato", "república",
        "prehistoria", "cronología", "fuente histórica", "perú", "incas",
        "españa", "coloniaje", "emancipación", "caudillo", "conflicto"
    ]
}

# ============================================================
# RECOMENDACIONES POR NIVEL — LENGUAJE CERCANO PARA ADOLESCENTES
# ============================================================

RECOMENDACIONES_BLOOM = {
    0: (
        "Tu pregunta pide solo recordar datos sueltos. "
        "¿Qué tal si das un paso más y preguntas por qué eso importa "
        "o cómo se usa en la vida real? Así el estudiante piensa más profundo."
    ),
    1: (
        "Bien, tu pregunta busca que el estudiante explique con sus propias palabras. "
        "Para hacerla más retadora, podrías pedir que la relacione con algo "
        "de su entorno o experiencia cotidiana."
    ),
    2: (
        "Buena pregunta de aplicación práctica. "
        "Para enriquecerla, dale un contexto concreto al estudiante: "
        "un problema real, una situación de su comunidad o un caso del aula."
    ),
    3: (
        "Excelente nivel de análisis. "
        "Para potenciarla, pide que el estudiante sustente su comparación "
        "con ejemplos o datos específicos del tema que está estudiando."
    ),
    4: (
        "Muy buena pregunta de evaluación crítica. "
        "Asegúrate de indicar qué criterios deben considerar para argumentar, "
        "así la respuesta del estudiante será más ordenada y fundamentada."
    ),
    5: (
        "¡Nivel máximo de pensamiento creativo! "
        "Para que sea aún más efectiva, define qué producto o propuesta se espera "
        "y con qué criterios se va a valorar el resultado."
    )
}

# ============================================================
# PLANTILLAS DE PREGUNTAS MEJORADAS POR NIVEL
# ============================================================

MEJORAS_BLOOM = {
    0: lambda tema: (
        f"¿Por qué es importante {tema} y de qué manera "
        f"lo podemos ver en nuestra vida cotidiana?"
    ),
    1: lambda tema: (
        f"¿Cómo explicarías {tema} con tus propias palabras "
        f"y qué ejemplo de tu entorno usarías para ilustrarlo?"
    ),
    2: lambda tema: (
        f"¿Cómo resolverías un problema real aplicando lo que sabes sobre {tema}? "
        f"Describe paso a paso lo que harías."
    ),
    3: lambda tema: (
        f"¿Cuáles son las principales semejanzas y diferencias en {tema}? "
        f"Sustenta tu respuesta con al menos dos ejemplos concretos."
    ),
    4: lambda tema: (
        f"¿Qué tan válido o relevante consideras {tema} en la actualidad? "
        f"Argumenta tu posición con al menos dos razones bien fundamentadas."
    ),
    5: lambda tema: (
        f"Diseña una propuesta o solución creativa relacionada con {tema}, "
        f"explicando los pasos que seguirías y qué resultados esperas lograr."
    )
}


# ============================================================
# FUNCIONES DE APOYO
# ============================================================

def _extraer_tema(pregunta: str) -> str:
    """Extrae el tema central de la pregunta eliminando los verbos de inicio."""
    p = pregunta.strip().rstrip("?").rstrip(".")
    eliminables = [
        "qué es", "define", "explica", "describe", "analiza", "compara",
        "evalúa", "diseña", "menciona", "identifica", "por qué", "cómo",
        "cuál es", "qué son", "cuáles son", "qué entiendes por",
        "en qué consiste", "resume", "justifica", "argumenta", "propone",
        "elabora", "construye", "crea", "redacta"
    ]
    p_lower = p.lower()
    for e in eliminables:
        if p_lower.startswith(e):
            resto = p[len(e):].strip()
            # Elimina artículos iniciales
            for articulo in ["la ", "el ", "los ", "las ", "un ", "una "]:
                if resto.lower().startswith(articulo):
                    resto = resto[len(articulo):]
                    break
            p = resto
            break
    tema = p[:65].strip()
    return tema if tema else pregunta[:65].strip()


def _detectar_curso(pregunta: str) -> str | None:
    """Detecta el curso más probable por vocabulario específico."""
    p = pregunta.lower()
    coincidencias = {}
    for curso, keywords in CURSOS_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in p)
        if score > 0:
            coincidencias[curso] = score
    if not coincidencias:
        return None
    return max(coincidencias, key=coincidencias.get)


def _clasificar_nivel_bloom(pregunta: str) -> int:
    """
    Clasifica la pregunta en uno de los 6 niveles de Bloom.
    Prioriza niveles cognitivos más altos ante ambigüedad.
    Retorna entero 0 (Recordar) … 5 (Crear).
    """
    p = pregunta.lower().strip()
    for nivel in sorted(NIVELES_BLOOM.keys(), reverse=True):
        if any(verbo in p for verbo in NIVELES_BLOOM[nivel]["verbos"]):
            return nivel
    return 1  # Comprender por defecto


NOMBRES_CURSOS = {
    "matematica": "Matemática",
    "geografia": "Geografía",
    "ciencia_tecnologia": "Ciencia y Tecnología",
    "educacion_civica": "Educación Cívica",
    "comunicacion": "Comunicación",
    "ingles": "Inglés",
    "computacion": "Computación",
    "historia": "Historia"
}


def _construir_feedback(nivel_idx: int, curso: str | None) -> str:
    """
    Construye feedback pedagógico claro y motivador
    adaptado a estudiantes de 2do de secundaria.
    """
    info = NIVELES_BLOOM[nivel_idx]
    nivel_num = nivel_idx + 1
    nombre = info["nombre"]
    descripcion = info["descripcion"]
    recomendacion = RECOMENDACIONES_BLOOM[nivel_idx]

    curso_txt = ""
    if curso:
        nombre_curso = NOMBRES_CURSOS.get(curso, curso)
        curso_txt = f" | Curso: {nombre_curso}"

    return (
        f"Nivel {nivel_num}/6 — {nombre}{curso_txt}. "
        f"{descripcion} "
        f"{recomendacion}"
    )


def _bloom_engine(question_text: str) -> dict:
    """
    Motor local de análisis basado en Taxonomía de Bloom
    contextualizado para estudiantes de 2do de secundaria.
    Retorna el mismo esquema que analyze_question.
    """
    nivel_idx = _clasificar_nivel_bloom(question_text)
    curso = _detectar_curso(question_text)
    info = NIVELES_BLOOM[nivel_idx]
    tema = _extraer_tema(question_text)

    return {
        "level": info["nivel_legado"],          # "bajo" | "medio" | "alto"
        "bloom_level": nivel_idx + 1,           # 1–6 (para uso futuro)
        "bloom_nombre": info["nombre"],
        "curso_detectado": curso,
        "feedback": _construir_feedback(nivel_idx, curso),
        "improved_question": MEJORAS_BLOOM[nivel_idx](tema)
    }


# ============================================================
# ADAPTADOR PRINCIPAL
# ============================================================

class NLPServiceAdapter:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")
        self.gemini_available = False

        try:

            if api_key:

                genai.configure(api_key=api_key)

                self.model = genai.GenerativeModel(
                    "gemini-2.5-flash"
                )

                self.gemini_available = True

        except Exception as e:

            logging.error(f"Gemini no disponible: {e}")

    def analyze_question(self, question_text: str) -> dict:

        if not self.gemini_available:

            logging.info(
                "Gemini no disponible — usando motor local Bloom (2do secundaria)."
            )
            return _bloom_engine(question_text)

        prompt = f"""
Evalúa esta pregunta de un estudiante de 2do de secundaria y responde SOLO JSON:

Pregunta:
{question_text}

Formato:
{{
 "level":"bajo|medio|alto",
 "feedback":"máximo 20 palabras",
 "improved_question":"versión mejorada"
}}
"""

        try:

            response = self.model.generate_content(prompt)

            raw = getattr(response, "text", "").strip()

            raw = raw.replace(
                "```json",
                ""
            ).replace(
                "```",
                ""
            ).strip()

            if "{" in raw:
                raw = raw[
                    raw.find("{"):
                    raw.rfind("}") + 1
                ]

            result = json.loads(raw)

            return {
                "level":
                result.get("level", "medio"),

                "feedback":
                result.get("feedback", ""),

                "improved_question":
                result.get(
                    "improved_question",
                    question_text
                )
            }

        except Exception as e:

            logging.error(
                f"Gemini fallback activado: {e} — usando motor local Bloom."
            )

            return _bloom_engine(question_text)