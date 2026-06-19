import logging
from datetime import timedelta

from flask import Blueprint, jsonify, request, make_response

from src.infrastructure.adapters.outbound.database.FirestoreRepository import FirestoreRepository
from src.infrastructure.adapters.inbound.middlewares.auth_middleware import require_auth

logger = logging.getLogger(__name__)
router = Blueprint("courses", __name__, url_prefix="/api/courses")


# ══════════════════════════════════════════════════════
# GET /api/courses  — HU-02
# ══════════════════════════════════════════════════════
@router.route("", methods=["GET"])
@require_auth
def get_courses():
    """Listar todos los cursos disponibles.
    ---
    tags:
      - Cursos
    security:
      - Bearer: []
    responses:
      200:
        description: Lista de cursos
        schema:
          type: object
          properties:
            success:
              type: boolean
            courses:
              type: array
              items:
                type: object
    """
    try:
        repo = FirestoreRepository()
        courses = repo.get_courses()
        logger.info("Cursos listados: %d encontrados", len(courses))
        response = make_response(jsonify({"success": True, "courses": courses}))
        response.cache_control.max_age = 3600
        response.cache_control.public = True
        return response, 200
    except Exception as e:
        logger.error("get_courses: error - %s", e, exc_info=True)
        return jsonify({"success": False, "error": str(e)}), 500


# ══════════════════════════════════════════════════════
# GET /api/courses/<course_id>/questions  — HU-15, HU-16, HU-17
# ══════════════════════════════════════════════════════
@router.route("/<course_id>/questions", methods=["GET"])
@require_auth
def get_questions_by_course(course_id):
    """Listar preguntas de un curso.
    ---
    tags:
      - Cursos
    security:
      - Bearer: []
    parameters:
      - name: course_id
        in: path
        type: string
        required: true
      - name: limit
        in: query
        type: integer
        default: 20
      - name: startAfter
        in: query
        type: string
    responses:
      200:
        description: Lista de preguntas del curso
    """
    try:
        repo = FirestoreRepository()
        limit_param = request.args.get("limit", 20, type=int)
        start_after = request.args.get("startAfter", None)
        limit_val = min(max(limit_param, 1), 100)
        questions = repo.get_questions_by_course(course_id, limit=limit_val, start_after=start_after)
        logger.info("Preguntas del curso %s: %d encontradas", course_id, len(questions))
        return jsonify({"success": True, "questions": questions}), 200
    except Exception as e:
        logger.error("get_questions_by_course %s: error - %s", course_id, e, exc_info=True)
        return jsonify({"success": False, "error": str(e)}), 500