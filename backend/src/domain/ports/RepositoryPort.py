from abc import ABC, abstractmethod
from typing import Optional


class RepositoryPort(ABC):

    # ── COURSES ──────────────────────────────────────────────
    @abstractmethod
    def get_courses(self) -> list[dict]:
        pass

    @abstractmethod
    def get_course_by_id(self, course_id: str) -> Optional[dict]:
        pass

    # ── QUESTIONS ────────────────────────────────────────────
    @abstractmethod
    def create_question(self, data: dict) -> dict:
        pass

    @abstractmethod
    def get_questions_by_course(self, course_id: str, limit: int = 20, start_after: str = None) -> list[dict]:
        pass

    @abstractmethod
    def get_question_by_id(self, question_id: str) -> Optional[dict]:
        pass

    @abstractmethod
    def get_question_by_idempotency_key(self, key: str) -> Optional[dict]:
        pass

    @abstractmethod
    def get_questions_by_user(self, user_id: str, limit: int = 20, start_after: str = None) -> list[dict]:
        pass

    @abstractmethod
    def update_question(self, question_id: str, data: dict) -> dict:
        pass

    @abstractmethod
    def delete_question(self, question_id: str) -> bool:
        pass

    # ── USERS ────────────────────────────────────────────────
    @abstractmethod
    def create_user_if_not_exists(self, user_data: dict) -> dict:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: str) -> Optional[dict]:
        pass
