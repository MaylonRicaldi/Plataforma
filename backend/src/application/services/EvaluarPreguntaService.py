from src.application.use_cases.EvaluarPreguntaUseCase import EvaluarPreguntaUseCase


class EvaluarPreguntaService:

    def __init__(self):
        self.use_case = EvaluarPreguntaUseCase()

    def obtener_detalle(self, question_id: str) -> dict:
        return self.use_case.execute(question_id)
