import logging

from flask import Blueprint, jsonify, request

from src.application.services.MejorarPreguntaService import MejorarPreguntaService
from src.infrastructure.adapters.inbound.middlewares.auth_middleware import require_auth

logger  = logging.getLogger(__name__)
router  = Blueprint("ai", __name__, url_prefix="/api/ai")
service = MejorarPreguntaService()


# ══════════════════════════════════════════════════════
# POST /api/ai/improve-question  — HU-12, HU-13, HU-22
# Previsualiza la mejora ANTES de guardar la pregunta
# ══════════════════════════════════════════════════════
@router.route("/improve-question", methods=["POST"])
@require_auth
def mejorar_pregunta():
    """Previsualizar mejora de pregunta con IA sin guardar.
    ---
    tags:
      - IA
    security:
      - Bearer: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            questionText:
              type: string
    responses:
      200:
        description: Analisis de la pregunta
      400:
        description: Error de validacion
    """
    try:
        data   = request.get_json()
        result = service.mejorar(data.get("questionText", ""))
        logger.info("Pregunta mejorada exitosamente")
        return jsonify({"success": True, "result": result}), 200

    except ValueError as e:
        logger.warning("mejorar_pregunta: validacion - %s", e)
        return jsonify({"success": False, "message": str(e)}), 400
    except Exception as e:
        logger.error("mejorar_pregunta: error interno - %s", e, exc_info=True)
        return jsonify({"success": False, "message": "Error al analizar pregunta", "error": str(e)}), 500
