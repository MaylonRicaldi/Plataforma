from flask import Blueprint
from flask import jsonify

from src.infrastructure.database.FirestoreRepository import FirestoreRepository


router = Blueprint(
    "courses",
    __name__,
    url_prefix="/api/courses"
)


repo = FirestoreRepository()


# -------------------------
# LISTAR CURSOS
# -------------------------

@router.route(
    "",
    methods=["GET"]
)
def get_courses():

    try:

        courses = repo.get_courses()

        return jsonify(
            {
                "success": True,
                "courses": courses
            }
        ), 200

    except Exception as e:

        return jsonify(
            {
                "success": False,
                "error": str(e)
            }
        ), 500


# -------------------------
# PREGUNTAS POR CURSO
# -------------------------

@router.route(
    "/<course_id>/questions",
    methods=["GET"]
)
def get_questions_by_course(
    course_id
):

    try:

        questions = repo.get_questions_by_course(
            course_id
        )

        return jsonify(
            {
                "success": True,
                "questions": questions
            }
        ), 200

    except Exception as e:

        return jsonify(
            {
                "success": False,
                "error": str(e)
            }
        ), 500
