from src.application.use_cases.AnalizarProgresoUseCase import AnalizarProgresoUseCase


class AnalizarProgresoService:

    def __init__(self):
        self.use_case = AnalizarProgresoUseCase()

    def analizar(self, user_id: str = None) -> dict:
        return self.use_case.execute(user_id=user_id)
