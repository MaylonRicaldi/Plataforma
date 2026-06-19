from src.domain.ports.AnalyticsPort import AnalyticsPort
from src.infrastructure.adapters.outbound.analytics.AnalyticsAdapter import AnalyticsAdapter


class AnalizarProgresoUseCase:
    """
    HU-18, HU-19, HU-22
    Calcula métricas reales de progreso académico del estudiante.
    """

    def __init__(self, analytics: AnalyticsPort = None):
        self.analytics = analytics or AnalyticsAdapter()

    def execute(self, user_id: str = None) -> dict:
        return self.analytics.analizar_progreso(user_id=user_id)
