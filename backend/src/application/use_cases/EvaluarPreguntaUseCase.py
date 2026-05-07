from src.infrastructure.database.FirestoreRepository import FirestoreRepository


class EvaluarPreguntaUseCase:

    def __init__(self):
        self.repository = FirestoreRepository()

    def execute(self, question_id):
        question = self.repository.get_question_by_id(question_id)

        if not question:
            raise ValueError("La pregunta no existe")

        return question
