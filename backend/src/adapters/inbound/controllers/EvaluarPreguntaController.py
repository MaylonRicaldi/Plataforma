from flask import Blueprint, jsonify

from src.application.services.EvaluarPreguntaService import EvaluarPreguntaService


router = Blueprint(
    "evaluar_pregunta",
    __name__,
    url_prefix="/api/questions"
)

service = EvaluarPreguntaService()


@router.route("/<question_id>", methods=["GET"])
def obtener_detalle_pregunta(question_id):
    try:
        question = service.obtener_detalle(question_id)

        return jsonify({
            "success": True,
            "question": question
        }), 200

    except ValueError as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 404

    except Exception as e:
        return jsonify({
            "success": False,
            "message": "Error al obtener pregunta",
            "error": str(e)
        }), 500
