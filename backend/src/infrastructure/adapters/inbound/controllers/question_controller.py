import logging

from flask import Blueprint, jsonify, request, g

from src.application.services.CrearPreguntaService import CrearPreguntaService
from src.application.services.EvaluarPreguntaService import EvaluarPreguntaService
from src.application.services.MejorarPreguntaService import MejorarPreguntaService
from src.infrastructure.adapters.outbound.database.FirestoreRepository import FirestoreRepository
from src.infrastructure.adapters.inbound.middlewares.auth_middleware import require_auth

logger = logging.getLogger(__name__)
security_logger = logging.getLogger("security")
router = Blueprint("questions", __name__, url_prefix="/api/questions")


# ══════════════════════════════════════════════════════
# POST /api/questions  — HU-01, HU-03, HU-04, HU-05, HU-06, HU-09, HU-11, HU-21
# ══════════════════════════════════════════════════════
@router.route("", methods=["POST"])
@require_auth
def crear_pregunta():
    """Crear una nueva pregunta con analisis de IA.
    ---
    tags:
      - Preguntas
    security:
      - Bearer: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            courseId:
              type: string
            questionText:
              type: string
            userId:
              type: string
            userName:
              type: string
            idempotencyKey:
              type: string
    responses:
      201:
        description: Pregunta creada y analizada
      400:
        description: Error de validacion
    """
    try:
        data = request.get_json(silent=True)
        
        if data is None:
            logger.warning("crear_pregunta: JSON malformado desde %s", request.remote_addr)
            return jsonify({
                "success": False, 
                "message": "El cuerpo de la solicitud no contiene un JSON valido o esta malformado."
            }), 400
        
        data["userId"] = g.uid
        crear_service = CrearPreguntaService()
        question = crear_service.crear(data)
        logger.info("Pregunta creada exitosamente: %s", question.get("id", "?"))
        
        return jsonify({
            "success":  True,
            "message":  "Pregunta creada y analizada correctamente",
            "question": question,
        }), 201

    except ValueError as e:
        logger.warning("crear_pregunta: error de validacion - %s", e)
        return jsonify({"success": False, "message": str(e)}), 400
    except Exception as e:
        logger.error("crear_pregunta: error interno - %s", e, exc_info=True)
        return jsonify({"success": False, "message": "Error al crear pregunta", "error": str(e)}), 500


# ══════════════════════════════════════════════════════
# GET /api/questions/<id>  — HU-07, HU-10, HU-15, HU-16
# ══════════════════════════════════════════════════════
@router.route("/<question_id>", methods=["GET"])
@require_auth
def obtener_pregunta(question_id):
    try:
        evaluar_service = EvaluarPreguntaService()
        question = evaluar_service.obtener_detalle(question_id)
        
        if not question:
            logger.info("obtener_pregunta: no encontrada id=%s", question_id)
            return jsonify({"success": False, "message": "La pregunta no existe"}), 404
            
        return jsonify({"success": True, "question": question}), 200

    except ValueError as e:
        logger.warning("obtener_pregunta: error - %s", e)
        return jsonify({"success": False, "message": str(e)}), 404
    except Exception as e:
        logger.error("obtener_pregunta: error interno id=%s - %s", question_id, e, exc_info=True)
        return jsonify({"success": False, "message": "Error al obtener pregunta", "error": str(e)}), 500


# ══════════════════════════════════════════════════════
# PUT /api/questions/<id>  — HU-14 (editar pregunta)
# ══════════════════════════════════════════════════════
@router.route("/<question_id>", methods=["PUT"])
@require_auth
def editar_pregunta(question_id):
    try:
        data = request.get_json(silent=True)
        
        if data is None:
            logger.warning("editar_pregunta: JSON malformado id=%s", question_id)
            return jsonify({
                "success": False, 
                "message": "El cuerpo de la solicitud no contiene un JSON valido o esta malformado."
            }), 400
            
        question_text = (data.get("questionText") or "").strip()

        if not question_text:
            logger.warning("editar_pregunta: texto vacio id=%s", question_id)
            return jsonify({"success": False, "message": "La pregunta no puede estar vacía"}), 400
        if len(question_text) < 10:
            logger.warning("editar_pregunta: texto demasiado corto id=%s", question_id)
            return jsonify({"success": False, "message": "La pregunta es demasiado corta"}), 400

        repo = FirestoreRepository()
        existing = repo.get_question_by_id(question_id)
        if not existing:
            return jsonify({"success": False, "message": "La pregunta no existe"}), 404
        if existing.get("userId") != g.uid:
            security_logger.warning("EVENTO=ACCESO_DENEGADO_EDITAR uid=%s pregunta=%s dueno=%s", g.uid, question_id, existing.get("userId"))
            return jsonify({"success": False, "message": "No tienes permiso para editar esta pregunta"}), 403

        mejorar_service = MejorarPreguntaService()

        ai_result = mejorar_service.mejorar(question_text)

        updated = repo.update_question(question_id, {
            "questionText":     question_text,
            "aiLevel":          ai_result["level"],
            "aiFeedback":       ai_result["feedback"],
            "improvedQuestion": ai_result["improved_question"],
            "bloomLevel":       ai_result.get("bloom_level"),
            "bloomNombre":      ai_result.get("bloom_nombre"),
            "cursoDetectado":   ai_result.get("curso_detectado"),
        })

        if not updated:
            logger.warning("editar_pregunta: no encontrada id=%s", question_id)
            return jsonify({"success": False, "message": "La pregunta no existe"}), 404

        logger.info("Pregunta actualizada exitosamente id=%s", question_id)
        return jsonify({"success": True, "message": "Pregunta actualizada", "question": updated}), 200

    except ValueError as e:
        logger.warning("editar_pregunta: error id=%s - %s", question_id, e)
        return jsonify({"success": False, "message": str(e)}), 404
    except Exception as e:
        logger.error("editar_pregunta: error interno id=%s - %s", question_id, e, exc_info=True)
        return jsonify({"success": False, "message": "Error al editar pregunta", "error": str(e)}), 500


# ══════════════════════════════════════════════════════
# DELETE /api/questions/<id>  — eliminar pregunta
# ══════════════════════════════════════════════════════
@router.route("/<question_id>", methods=["DELETE"])
@require_auth
def eliminar_pregunta(question_id):
    try:
        repo = FirestoreRepository()
        existing = repo.get_question_by_id(question_id)
        if not existing:
            return jsonify({"success": False, "message": "La pregunta no existe"}), 404
        if existing.get("userId") != g.uid:
            security_logger.warning("EVENTO=ACCESO_DENEGADO_ELIMINAR uid=%s pregunta=%s dueno=%s", g.uid, question_id, existing.get("userId"))
            return jsonify({"success": False, "message": "No tienes permiso para eliminar esta pregunta"}), 403
        deleted = repo.delete_question(question_id)
        logger.info("Pregunta eliminada exitosamente: %s", question_id)
        return jsonify({"success": True, "message": "Pregunta eliminada"}), 200
    except Exception as e:
        logger.error("eliminar_pregunta: error - %s", e, exc_info=True)
        return jsonify({"success": False, "error": str(e)}), 500


# ══════════════════════════════════════════════════════
# GET /api/questions/user/<user_id>  — HU-15, HU-18, HU-19
# ══════════════════════════════════════════════════════
@router.route("/user/<user_id>", methods=["GET"])
@require_auth
def obtener_preguntas_usuario(user_id):
    if user_id != g.uid:
        security_logger.warning("EVENTO=ACCESO_DENEGADO_IDOR uid=%s intento_acceder=%s", g.uid, user_id)
        return jsonify({"success": False, "message": "No tienes permiso para ver las preguntas de otro usuario"}), 403
    try:
        repo = FirestoreRepository()
        limit_param = request.args.get("limit", 20, type=int)
        start_after = request.args.get("startAfter", None)
        limit_val = min(max(limit_param, 1), 100)
        questions = repo.get_questions_by_user(user_id, limit=limit_val, start_after=start_after)
        logger.info("Preguntas listadas para usuario %s: %d encontradas", user_id, len(questions))
        return jsonify({"success": True, "questions": questions}), 200
    except Exception as e:
        logger.error("obtener_preguntas_usuario: error para %s - %s", user_id, e, exc_info=True)
        return jsonify({"success": False, "error": str(e)}), 500