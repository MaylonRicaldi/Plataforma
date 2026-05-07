from src.infrastructure.ai.NLPServiceAdapter import NLPServiceAdapter


class MejorarPreguntaUseCase:

    def __init__(self):
        self.nlp_service = NLPServiceAdapter()

    def execute(self, question_text):
        if not question_text:
            raise ValueError("La pregunta es obligatoria")

        return self.nlp_service.analyze_question(question_text)
