import unicodedata

import spacy

_nlp = None


def _get_nlp():
    global _nlp
    if _nlp is None:
        try:
            _nlp = spacy.load("es_core_news_sm")
        except OSError:
            _nlp = False
    return _nlp


def quitar_acentos(texto: str) -> str:
    texto = texto.lower()
    return "".join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )


def lematizar(texto: str) -> str:
    nlp = _get_nlp()
    if nlp is False:
        return quitar_acentos(texto)
    doc = nlp(texto.lower())
    return " ".join(token.lemma_ for token in doc)


def extraer_tema(pregunta: str) -> str:
    p = pregunta.strip().rstrip("?").rstrip(".").lstrip("\u00bf")
    eliminables = [
        "qué es", "define", "explica", "describe", "analiza", "compara",
        "evalúa", "diseña", "menciona", "identifica", "por qué", "cómo",
        "cuál es", "qué son", "cuáles son", "qué entiendes por",
        "en qué consiste", "resume", "justifica", "argumenta", "propone",
        "elabora", "construye", "crea", "redacta",
    ]
    p_lower = p.lower()
    for e in eliminables:
        if p_lower.startswith(e):
            resto = p[len(e):].strip()
            for art in ["la ", "el ", "los ", "las ", "un ", "una "]:
                if resto.lower().startswith(art):
                    resto = resto[len(art):]
                    break
            p = resto
            break
    if len(p) > 65:
        p = p[:65].rsplit(" ", 1)[0]
    tema = p.strip()
    return tema if tema else pregunta[:65].strip()
