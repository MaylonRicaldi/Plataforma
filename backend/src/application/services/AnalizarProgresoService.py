from src.application.use_cases.AnalizarProgresoUseCase import AnalizarProgresoUseCase


class AnalizarProgresoService:

    def __init__(self):
        self.use_case = AnalizarProgresoUseCase()

    def analizar(self):
        return self.use_case.execute()
