from abc import ABC, abstractmethod


class RepositoryPort(ABC):

    @abstractmethod
    def get_courses(self):
        pass

    @abstractmethod
    def get_course_by_id(self, course_id):
        pass

    @abstractmethod
    def create_question(self, data):
        pass

    @abstractmethod
    def get_questions_by_course(self, course_id):
        pass

    @abstractmethod
    def get_question_by_id(self, question_id):
        pass
