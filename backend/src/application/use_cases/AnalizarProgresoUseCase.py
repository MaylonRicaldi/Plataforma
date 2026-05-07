from src.infrastructure.database.FirestoreRepository import FirestoreRepository


class AnalizarProgresoUseCase:

    def __init__(self):
        self.repository = FirestoreRepository()

    def execute(self):
        courses = self.repository.get_courses()

        return {
            "totalCourses": len(courses),
            "message": "Análisis básico de progreso activo"
        }
