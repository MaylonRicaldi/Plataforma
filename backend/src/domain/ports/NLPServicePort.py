from abc import ABC, abstractmethod


class NLPServicePort(ABC):

    @abstractmethod
    def analyze_question(self, question_text):
        pass
