from flask import Blueprint, jsonify

from src.application.services.AnalizarProgresoService import AnalizarProgresoService


router = Blueprint(
    "analizar_progreso",
    __name__,
    url_prefix="/api/progress"
)

service = AnalizarProgresoService()


@router.route("", methods=["GET"])
def analizar_progreso():
    result = service.analizar()

    return jsonify({
        "success": True,
        "result": result
    }), 200
