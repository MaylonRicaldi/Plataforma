import logging

from flask import Blueprint, jsonify, request, g

from src.application.services.AnalizarProgresoService import AnalizarProgresoService
from src.infrastructure.adapters.inbound.middlewares.auth_middleware import require_auth

logger  = logging.getLogger(__name__)
router  = Blueprint("progress", __name__, url_prefix="/api/progress")
service = AnalizarProgresoService()


# ══════════════════════════════════════════════════════
# GET /api/progress  — HU-18, HU-19
# GET /api/progress?userId=<uid>  — filtrar por usuario
# ══════════════════════════════════════════════════════
@router.route("", methods=["GET"])
@require_auth
def analizar_progreso():
    """Obtener metricas de progreso del usuario.
    ---
    tags:
      - Progreso
    security:
      - Bearer: []
    parameters:
      - name: userId
        in: query
        type: string
        required: false
    responses:
      200:
        description: Metricas de progreso
    """
    try:
        user_id = g.uid
        result  = service.analizar(user_id=user_id)
        logger.info("Progreso analizado para usuario %s", user_id)
        return jsonify({"success": True, "result": result}), 200

    except Exception as e:
        logger.error("analizar_progreso: error - %s", e, exc_info=True)
        return jsonify({"success": False, "error": str(e)}), 500
