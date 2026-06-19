from src.domain.ports.AnalyticsPort import AnalyticsPort
from src.infrastructure.adapters.outbound.database.FirestoreRepository import FirestoreRepository


class AnalyticsAdapter(AnalyticsPort):

    def __init__(self):
        self.repo = FirestoreRepository()

    def analizar_progreso(self, user_id: str = None) -> dict:
        """
        Calcula métricas reales desde Firestore.
        Si se pasa user_id, filtra solo las preguntas de ese usuario.
        """
        if user_id:
            questions = self.repo.get_questions_by_user(user_id)
        else:
            questions = self.repo.get_all_questions(limit=1000)

        total = len(questions)

        niveles = {"bajo": 0, "medio": 0, "alto": 0}
        bloom_counts = {i: 0 for i in range(1, 7)}

        for q in questions:
            nivel = q.get("aiLevel", "").lower()
            if nivel in niveles:
                niveles[nivel] += 1

            bl = q.get("bloomLevel")
            if bl and 1 <= bl <= 6:
                bloom_counts[bl] += 1

        # Nivel promedio por mayoría
        nivel_promedio = max(niveles, key=niveles.get) if total > 0 else "sin datos"

        # Bloom level promedio
        bloom_total = sum(k * v for k, v in bloom_counts.items())
        bloom_avg   = round(bloom_total / total, 2) if total > 0 else 0

        # Evolución: últimas 10 preguntas con su nivel
        evolucion = [
            {
                "id":        q.get("id"),
                "nivel":     q.get("aiLevel", ""),
                "bloomLevel": q.get("bloomLevel"),
                "fecha":     str(q.get("createdAt", "")),
            }
            for q in questions[:10]
        ]

        return {
            "totalPreguntas":  total,
            "nivelPromedio":   nivel_promedio,
            "nivelesDetalle":  niveles,
            "bloomPromedio":   bloom_avg,
            "bloomDetalle":    bloom_counts,
            "evolucion":       evolucion,
        }
