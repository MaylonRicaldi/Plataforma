from abc import ABC, abstractmethod


class AnalyticsPort(ABC):

    @abstractmethod
    def analizar_progreso(self, user_id: str = None) -> dict:
        """
        Retorna métricas de progreso académico.
        Si user_id es None, retorna estadísticas globales.
        """
        pass
