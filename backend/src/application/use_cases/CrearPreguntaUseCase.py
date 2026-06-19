import logging

from src.domain.ports.RepositoryPort import RepositoryPort
from src.domain.ports.NLPServicePort import NLPServicePort
from src.infrastructure.adapters.outbound.database.FirestoreRepository import FirestoreRepository
from src.infrastructure.adapters.outbound.ai.NLPServiceAdapter import NLPServiceAdapter

logger = logging.getLogger(__name__)


class CrearPreguntaUseCase:
    """
    HU-01, HU-02, HU-03, HU-04, HU-05, HU-06, HU-08, HU-09, HU-11, HU-21
    Valida, analiza con IA y persiste una nueva pregunta.
    """

    def __init__(
        self,
        repository: RepositoryPort = None,
        nlp_service: NLPServicePort = None,
    ):
        self.repository  = repository  or FirestoreRepository()
        self.nlp_service = nlp_service or NLPServiceAdapter()

    def execute(self, data: dict) -> dict:
        course_id       = (data.get("courseId") or "").strip()
        question_text   = (data.get("questionText") or "").strip()
        user_id         = (data.get("userId") or "").strip()
        user_name       = (data.get("userName") or "Estudiante").strip()
        idempotency_key = (data.get("idempotencyKey") or "").strip()

        if not course_id:
            raise ValueError("El curso es obligatorio")
        if not question_text:
            raise ValueError("La pregunta no puede estar vacía")
        if len(question_text) < 10:
            raise ValueError("La pregunta es demasiado corta (mínimo 10 caracteres)")

        course = self.repository.get_course_by_id(course_id)
        if not course:
            raise ValueError("El curso seleccionado no existe")

        if idempotency_key:
            existing = self.repository.get_question_by_idempotency_key(idempotency_key)
            if existing:
                return existing

        ai_result = self.nlp_service.analyze_question(question_text)

        if not isinstance(ai_result, dict):
            logger.error("NLP devolvio un tipo inesperado: %s", type(ai_result))
            raise ValueError("Error al analizar la pregunta con IA")

        question_data = {
            "courseId":         course_id,
            "courseName":       course.get("name", ""),
            "userId":           user_id,
            "userName":         user_name,
            "questionText":     question_text,
            "aiLevel":          ai_result.get("level", "bajo"),
            "aiFeedback":       ai_result.get("feedback", ""),
            "improvedQuestion": ai_result.get("improved_question", question_text),
            "bloomLevel":       ai_result.get("bloom_level"),
            "bloomNombre":      ai_result.get("bloom_nombre"),
            "cursoDetectado":   ai_result.get("curso_detectado"),
        }

        if idempotency_key:
            question_data["idempotencyKey"] = idempotency_key

        return self.repository.create_question(question_data)
