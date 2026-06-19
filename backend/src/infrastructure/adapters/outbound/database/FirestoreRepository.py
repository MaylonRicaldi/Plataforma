import logging
import time
from datetime import datetime, timezone
from typing import Optional

from google.api_core.exceptions import (
    DeadlineExceeded,
    ResourceExhausted,
    ServiceUnavailable,
    InternalServerError,
)

from src.domain.ports.RepositoryPort import RepositoryPort
from src.infrastructure.config.firebase_config import db

logger = logging.getLogger(__name__)

RETRYABLE_EXCEPTIONS = (DeadlineExceeded, ResourceExhausted, ServiceUnavailable, InternalServerError)
MAX_RETRIES = 3
INITIAL_BACKOFF = 0.5


def _firestore_retry(operation_name: str):
    """Decorator que reintenta operaciones Firestore con backoff exponencial."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, MAX_RETRIES + 1):
                try:
                    return func(*args, **kwargs)
                except RETRYABLE_EXCEPTIONS as e:
                    last_exc = e
                    if attempt < MAX_RETRIES:
                        backoff = INITIAL_BACKOFF * (2 ** (attempt - 1))
                        logger.warning(
                            "%s: intento %d/%d fallo (%s), reintentando en %.1fs",
                            operation_name, attempt, MAX_RETRIES, e, backoff,
                        )
                        time.sleep(backoff)
                    else:
                        logger.error(
                            "%s: agotados %d reintentos - %s",
                            operation_name, MAX_RETRIES, e, exc_info=True,
                        )
            raise last_exc
        return wrapper
    return decorator


class FirestoreRepository(RepositoryPort):

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "db"):
            self.db = db

    # ═══════════════════════════════════════════════════════
    # USERS
    # ═══════════════════════════════════════════════════════

    @_firestore_retry("create_user_if_not_exists")
    def create_user_if_not_exists(self, user_data: dict) -> dict:
        uid      = user_data["uid"]
        user_ref = self.db.collection("users").document(uid)
        user_doc = user_ref.get()

        if user_doc.exists:
            data      = user_doc.to_dict()
            data["id"] = uid
            return data

        now = datetime.now(timezone.utc)
        new_user = {
            "uid":       uid,
            "email":     user_data.get("email", ""),
            "name":      user_data.get("name", user_data.get("email", "")),
            "role":      "student",
            "createdAt": now,
            "updatedAt": now,
        }
        user_ref.set(new_user)
        return new_user

    @_firestore_retry("get_user_by_id")
    def get_user_by_id(self, user_id: str) -> Optional[dict]:
        doc = self.db.collection("users").document(user_id).get()
        if not doc.exists:
            return None
        data      = doc.to_dict()
        data["id"] = doc.id
        return data

    # ═══════════════════════════════════════════════════════
    # COURSES
    # ═══════════════════════════════════════════════════════

    @_firestore_retry("get_courses")
    def get_courses(self) -> list[dict]:
        docs    = self.db.collection("courses").stream()
        courses = []
        for doc in docs:
            data      = doc.to_dict()
            data["id"] = doc.id
            courses.append(data)
        return courses

    @_firestore_retry("get_course_by_id")
    def get_course_by_id(self, course_id: str) -> Optional[dict]:
        doc = self.db.collection("courses").document(course_id).get()
        if not doc.exists:
            return None
        data      = doc.to_dict()
        data["id"] = doc.id
        return data

    # ═══════════════════════════════════════════════════════
    # QUESTIONS
    # ═══════════════════════════════════════════════════════

    @_firestore_retry("create_question")
    def create_question(self, data: dict) -> dict:
        ref = self.db.collection("questions").document()
        now = datetime.now(timezone.utc)
        data["createdAt"] = now
        data["updatedAt"] = now
        with self.db.transaction() as txn:
            txn.set(ref, data)
        data["id"] = ref.id
        logger.info("Pregunta creada en Firestore: %s", ref.id)
        return data

    @_firestore_retry("get_questions_by_course")
    def get_questions_by_course(self, course_id: str, limit: int = 20, start_after: str = None) -> list[dict]:
        query = (
            self.db.collection("questions")
            .where("courseId", "==", course_id)
            .order_by("createdAt", direction="DESCENDING")
            .limit(limit)
        )
        if start_after:
            doc_snapshot = self.db.collection("questions").document(start_after).get()
            if doc_snapshot.exists:
                query = query.start_after(doc_snapshot)

        docs = query.stream()
        questions = []
        for doc in docs:
            data      = doc.to_dict()
            data["id"] = doc.id
            questions.append(data)
        return questions

    @_firestore_retry("get_question_by_id")
    def get_question_by_id(self, question_id: str) -> Optional[dict]:
        doc = self.db.collection("questions").document(question_id).get()
        if not doc.exists:
            logger.info("Pregunta no encontrada: %s", question_id)
            return None
        data      = doc.to_dict()
        data["id"] = doc.id
        return data

    @_firestore_retry("get_question_by_idempotency_key")
    def get_question_by_idempotency_key(self, key: str) -> Optional[dict]:
        docs = (
            self.db.collection("questions")
            .where("idempotencyKey", "==", key)
            .limit(1)
            .stream()
        )
        for doc in docs:
            data      = doc.to_dict()
            data["id"] = doc.id
            return data
        return None

    @_firestore_retry("get_questions_by_user")
    def get_questions_by_user(self, user_id: str, limit: int = 20, start_after: str = None) -> list[dict]:
        query = (
            self.db.collection("questions")
            .where("userId", "==", user_id)
            .order_by("createdAt", direction="DESCENDING")
            .limit(limit)
        )
        if start_after:
            doc_snapshot = self.db.collection("questions").document(start_after).get()
            if doc_snapshot.exists:
                query = query.start_after(doc_snapshot)

        docs = query.stream()
        questions = []
        for doc in docs:
            data      = doc.to_dict()
            data["id"] = doc.id
            questions.append(data)
        return questions

    @_firestore_retry("update_question")
    def update_question(self, question_id: str, data: dict) -> dict:
        ref = self.db.collection("questions").document(question_id)
        doc = ref.get()
        if not doc.exists:
            logger.warning("Intento de actualizar pregunta inexistente: %s", question_id)
            raise ValueError("La pregunta no existe")

        data["updatedAt"] = datetime.now(timezone.utc)
        with self.db.transaction() as txn:
            txn.update(ref, data)

        updated      = ref.get().to_dict()
        updated["id"] = question_id
        logger.info("Pregunta actualizada: %s", question_id)
        return updated

    @_firestore_retry("delete_question")
    def delete_question(self, question_id: str) -> bool:
        ref = self.db.collection("questions").document(question_id)
        doc = ref.get()
        if not doc.exists:
            logger.warning("Intento de eliminar pregunta inexistente: %s", question_id)
            return False
        ref.delete()
        logger.info("Pregunta eliminada: %s", question_id)
        return True

    def get_all_questions(self, limit: int = 1000) -> list[dict]:
        docs = self.db.collection("questions").order_by("createdAt", direction="DESCENDING").limit(limit).stream()
        questions = []
        for doc in docs:
            data = doc.to_dict()
            data["id"] = doc.id
            questions.append(data)
        return questions

    # ═══════════════════════════════════════════════════════
    # ANALYTICS HELPERS
    # ═══════════════════════════════════════════════════════

    def count_questions_by_user(self, user_id: str) -> int:
        from google.cloud.firestore import aggregation
        query = self.db.collection("questions").where("userId", "==", user_id)
        results = list(query.count().get())
        return results[0][0].value if results else 0
