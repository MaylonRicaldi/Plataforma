from src.domain.ports.RepositoryPort import RepositoryPort
from src.infrastructure.adapters.outbound.database.FirestoreRepository import FirestoreRepository


class EvaluarPreguntaUseCase:
    """
    HU-07, HU-10, HU-15, HU-16
    Obtiene el detalle completo de una pregunta incluyendo análisis IA.
    """

    def __init__(self, repository: RepositoryPort = None):
        self.repository = repository or FirestoreRepository()

    def execute(self, question_id: str) -> dict:
        if not question_id:
            raise ValueError("El ID de la pregunta es obligatorio")

        question = self.repository.get_question_by_id(question_id)
        if not question:
            raise ValueError("La pregunta no existe")

        return question
