from flask import Blueprint, request, jsonify

from src.application.services.CrearPreguntaService import CrearPreguntaService


router = Blueprint(
    "crear_pregunta",
    __name__,
    url_prefix="/api/questions"
)

service = CrearPreguntaService()


@router.route("", methods=["POST"])
def crear_pregunta():
    try:
        data = request.get_json()

        question = service.crear(data)

        return jsonify({
            "success": True,
            "message": "Pregunta creada correctamente",
            "question": question
        }), 201

    except ValueError as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 400

    except Exception as e:
        return jsonify({
            "success": False,
            "message": "Error al crear pregunta",
            "error": str(e)
        }), 500
