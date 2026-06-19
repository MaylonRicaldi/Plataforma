from src.domain.ports.NLPServicePort import NLPServicePort
from src.infrastructure.adapters.outbound.ai.NLPServiceAdapter import NLPServiceAdapter


class MejorarPreguntaUseCase:
    """
    HU-12, HU-13, HU-22
    Analiza y sugiere una versión mejorada de la pregunta sin persistir.
    Útil para el botón "Mejorar antes de enviar".
    """

    def __init__(self, nlp_service: NLPServicePort = None):
        self.nlp_service = nlp_service or NLPServiceAdapter()

    def execute(self, question_text: str) -> dict:
        if not question_text or not question_text.strip():
            raise ValueError("La pregunta es obligatoria")
        if len(question_text.strip()) < 5:
            raise ValueError("La pregunta es demasiado corta")

        return self.nlp_service.analyze_question(question_text.strip())
