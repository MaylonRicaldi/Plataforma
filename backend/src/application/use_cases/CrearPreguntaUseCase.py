from src.infrastructure.database.FirestoreRepository import FirestoreRepository
from src.infrastructure.ai.NLPServiceAdapter import NLPServiceAdapter


class CrearPreguntaUseCase:

    def __init__(self):
        self.repository = FirestoreRepository()
        self.nlp_service = NLPServiceAdapter()

    def execute(self, data):
        course_id = data.get("courseId")
        question_text = data.get("questionText")
        user_id = data.get("userId", "")
        user_name = data.get("userName", "Estudiante")

        if not course_id:
            raise ValueError("El curso es obligatorio")

        if not question_text:
            raise ValueError("La pregunta es obligatoria")

        course = self.repository.get_course_by_id(course_id)

        if not course:
            raise ValueError("El curso no existe")

        ai_result = self.nlp_service.analyze_question(question_text)

        question_data = {
            "courseId": course_id,
            "courseName": course.get("name", ""),
            "userId": user_id,
            "userName": user_name,
            "questionText": question_text,
            "aiLevel": ai_result["level"],
            "aiFeedback": ai_result["feedback"],
            "improvedQuestion": ai_result["improved_question"]
        }

        return self.repository.create_question(question_data)
