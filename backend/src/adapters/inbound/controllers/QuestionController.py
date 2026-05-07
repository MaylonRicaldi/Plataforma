from flask import Blueprint
from flask import jsonify

from src.infrastructure.database.FirestoreRepository import FirestoreRepository


router = Blueprint(
    "question_detail",
    __name__
)


repo = FirestoreRepository()


@router.route(
    "/api/questions/<question_id>",
    methods=["GET"]
)
def get_question_detail(
    question_id
):

    try:

        question = repo.get_question_by_id(
            question_id
        )

        if not question:

            return jsonify(
                {
                    "success": False,
                    "message": "Pregunta no encontrada"
                }
            ), 404

        return jsonify(
            {
                "success": True,
                "question": question
            }
        ), 200

    except Exception as e:

        return jsonify(
            {
                "success": False,
                "error": str(e)
            }
        ), 500
