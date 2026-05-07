from src.application.use_cases.CrearPreguntaUseCase import CrearPreguntaUseCase


class CrearPreguntaService:

    def __init__(self):
        self.use_case = CrearPreguntaUseCase()

    def crear(self, data):
        return self.use_case.execute(data)
