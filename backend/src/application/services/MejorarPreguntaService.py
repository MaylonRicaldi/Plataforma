from src.application.use_cases.MejorarPreguntaUseCase import MejorarPreguntaUseCase


class MejorarPreguntaService:

    def __init__(self):
        self.use_case = MejorarPreguntaUseCase()

    def mejorar(self, question_text):
        return self.use_case.execute(question_text)
