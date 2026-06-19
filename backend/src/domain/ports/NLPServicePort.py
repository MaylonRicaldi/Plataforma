from abc import ABC, abstractmethod


class NLPServicePort(ABC):

    @abstractmethod
    def analyze_question(self, question_text: str) -> dict:
        """
        Analiza una pregunta y retorna:
        {
            "level":            "bajo" | "medio" | "alto",
            "bloom_level":      1..6,
            "bloom_nombre":     str,
            "curso_detectado":  str | None,
            "feedback":         str,
            "improved_question": str,
        }
        """
        pass
