from flask import Blueprint, request, jsonify

from src.application.services.MejorarPreguntaService import MejorarPreguntaService


router = Blueprint(
    "mejorar_pregunta",
    __name__,
    url_prefix="/api/ai"
)

service = MejorarPreguntaService()


@router.route("/improve-question", methods=["POST"])
def mejorar_pregunta():
    try:
        data = request.get_json()

        result = service.mejorar(
            data.get("questionText")
        )

        return jsonify({
            "success": True,
            "result": result
        }), 200

    except ValueError as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 400

    except Exception as e:
        return jsonify({
            "success": False,
            "message": "Error al mejorar pregunta",
            "error": str(e)
        }), 500
