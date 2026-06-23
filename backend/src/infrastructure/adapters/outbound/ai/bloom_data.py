NIVELES_BLOOM = {
    0: {
        "nombre":      "Recordar",
        "nivel_legado": "bajo",
        "descripcion": "El estudiante recupera información básica de memoria.",
        "verbos": [
            "qué es", "define", "definir", "qué son", "cuál es", "cuáles son",
            "menciona", "mencionar", "lista", "listar", "nombra", "nombrar",
            "identifica", "identificar", "enuncia", "enunciar", "reconoce",
            "señala", "señalar", "escribe", "cuándo", "dónde ocurrió",
            "quién fue", "qué significa",
        ],
    },
    1: {
        "nombre":      "Comprender",
        "nivel_legado": "bajo",
        "descripcion": "El estudiante demuestra que entiende el concepto con sus propias palabras.",
        "verbos": [
            "explica", "explicar", "describe", "describir", "resume", "resumir",
            "cómo funciona", "cómo se produce", "cómo ocurre", "interpreta",
            "interpretar", "clasifica", "clasificar", "parafrasea", "ilustra",
            "relaciona", "relata", "por qué ocurre", "en qué consiste",
            "qué entiendes", "qué significa para ti",
        ],
    },
    2: {
        "nombre":      "Aplicar",
        "nivel_legado": "medio",
        "descripcion": "El estudiante usa lo aprendido para resolver una situación concreta.",
        "verbos": [
            "aplica", "aplicar", "usa", "utiliza", "utilizar", "resuelve",
            "resolver", "implementa", "demuestra", "calcula", "calcular",
            "ejecuta", "construye", "desarrolla", "emplea", "practica",
            "realiza", "efectúa", "opera", "si tuvieras que", "cómo usarías",
            "en qué caso", "cómo resolverías", "cómo aplicarías",
            "demuestra que", "halla", "determina", "determinar", "obtén",
            "haz", "cómo harías", "cómo aplicas", "cómo usas", "cómo solucionas",
            "cómo lo harías", "cómo lo resuelves",
        ],
    },
    3: {
        "nombre":      "Analizar",
        "nivel_legado": "medio",
        "descripcion": "El estudiante descompone información y examina sus partes y relaciones.",
        "verbos": [
            "analiza", "analizar", "compara", "comparar", "diferencia",
            "diferenciar", "examina", "examinar", "descompone", "distingue",
            "distinguir", "organiza", "organizar", "contrasta", "contrastar",
            "estructura", "por qué crees", "qué relación existe",
            "en qué se parecen", "en qué se diferencian", "qué factores",
            "qué causas", "qué consecuencias", "cómo se relaciona",
            "qué relación hay", "compara y contrasta", "infiere", "inferir",
            "deduce", "deducir", "cómo afecta", "qué pasaría si",
            "cuál es la causa", "cuál es el efecto", "qué semejanzas",
            "qué diferencias", "cómo influye", "cómo impacta", "qué implica",
            "qué ocurre cuando", "qué sucede si", "cuál es la relación",
            "por qué sucede", "por qué ocurre", "explica por qué",
        ],
    },
    4: {
        "nombre":      "Evaluar",
        "nivel_legado": "alto",
        "descripcion": "El estudiante emite un juicio razonado usando criterios.",
        "verbos": [
            "evalúa", "evaluar", "critica", "criticar", "justifica",
            "justificar", "argumenta", "argumentar", "valora", "valorar",
            "defiende", "defender", "juzga", "recomienda", "recomendar",
            "prioriza", "fundamenta", "opina", "qué opinas", "estás de acuerdo",
            "consideras que", "por qué es importante", "qué tan válido",
            "cuál sería mejor", "cómo mejorarías", "qué tan correcto",
            "debate", "discute", "critica", "selecciona la mejor",
            "ordena por importancia", "qué prefieres", "cuál es mejor",
            "qué tan efectivo", "qué tan útil", "qué tan adecuado",
            "qué criterios usarías", "cómo evaluarías", "qué te parece",
        ],
    },
    5: {
        "nombre":      "Crear",
        "nivel_legado": "alto",
        "descripcion": "El estudiante produce algo nuevo combinando lo aprendido.",
        "verbos": [
            "diseña", "diseñar", "crea", "crear", "propone", "proponer",
            "formula", "formular", "planifica", "planificar", "genera",
            "elabora", "elaborar", "inventa", "inventar", "desarrolla un",
            "construye un", "escribe un", "redacta", "produce", "imagina",
            "cómo crearías", "qué propondrías", "si pudieras diseñar",
            "compón", "inventa un", "desarrolla una solución",
            "propón una alternativa", "imagina que", "diseña un",
            "crea un", "elabora un", "propón una idea",
            "cómo solucionarías", "qué crearías", "qué diseñarías",
        ],
    },
}

RECOMENDACIONES_BLOOM = {
    0: (
        "Tu pregunta pide solo recordar datos. "
        "Intenta preguntar por qué ese dato importa o cómo se aplica en la vida real."
    ),
    1: (
        "Bien, buscas que el estudiante explique con sus propias palabras. "
        "Para profundizar, pídele que relacione el concepto con algo de su entorno."
    ),
    2: (
        "Buena pregunta de aplicación. "
        "Dale un contexto concreto: un problema real o una situación de su comunidad."
    ),
    3: (
        "Excelente nivel de análisis. "
        "Pide que sustente su comparación con ejemplos o datos específicos del tema."
    ),
    4: (
        "Muy buena pregunta crítica. "
        "Indica qué criterios deben usar para argumentar; así la respuesta será más ordenada."
    ),
    5: (
        "¡Nivel máximo de pensamiento creativo! "
        "Define qué producto se espera y con qué criterios se valorará el resultado."
    ),
}

MEJORAS_BLOOM = {
    0: lambda t: f"¿Por qué es importante {t} y de qué manera lo vemos en la vida cotidiana?",
    1: lambda t: f"¿Cómo explicarías {t} con tus propias palabras y qué ejemplo usarías?",
    2: lambda t: f"¿Cómo resolverías un problema real aplicando lo que sabes sobre {t}?",
    3: lambda t: f"¿Cuáles son las principales semejanzas y diferencias en {t}? Sustenta con dos ejemplos.",
    4: lambda t: f"¿Qué tan válido consideras {t} hoy? Argumenta con al menos dos razones fundamentadas.",
    5: lambda t: f"Diseña una propuesta creativa relacionada con {t}, explicando pasos y resultados esperados.",
}
