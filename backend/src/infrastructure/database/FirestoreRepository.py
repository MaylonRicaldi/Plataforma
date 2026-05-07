from datetime import datetime, timezone

from src.config.firebase_config import db


class FirestoreRepository:

    def __init__(self):
        self.db = db

    # ==================================
    # USERS
    # ==================================

    def create_user_if_not_exists(
        self,
        user_data
    ):

        uid = user_data["uid"]

        user_ref = self.db.collection(
            "users"
        ).document(
            uid
        )

        user_doc = user_ref.get()

        if user_doc.exists:

            data = user_doc.to_dict()

            data["uid"] = uid

            return data

        new_user = {

            "uid": uid,

            "email":
            user_data.get(
                "email",
                ""
            ),

            "name":
            user_data.get(
                "name",
                ""
            ),

            "role": "student",

            "createdAt": datetime.now(timezone.utc),
            "updatedAt": datetime.now(timezone.utc),

        }

        user_ref.set(
            new_user
        )

        return new_user

    # ==================================
    # COURSES
    # ==================================

    def get_courses(self):

        docs = self.db.collection(
            "courses"
        ).stream()

        courses = []

        for doc in docs:

            data = doc.to_dict()

            data["id"] = doc.id

            courses.append(
                data
            )

        return courses

    def get_course_by_id(
        self,
        course_id
    ):

        doc = self.db.collection(
            "courses"
        ).document(
            course_id
        ).get()

        if not doc.exists:
            return None

        data = doc.to_dict()

        data["id"] = doc.id

        return data

    # ==================================
    # QUESTIONS
    # ==================================

    def create_question(
        self,
        data
    ):

        ref = self.db.collection(
            "questions"
        ).document()

        data["createdAt"] = datetime.now(timezone.utc)
        data["updatedAt"] = datetime.now(timezone.utc)

        ref.set(
            data
        )

        data["id"] = ref.id

        return data

    def get_questions_by_course(
        self,
        course_id
    ):

        docs = (
            self.db.collection(
                "questions"
            )
            .where(
                "courseId",
                "==",
                course_id
            )
            .stream()
        )

        questions = []

        for doc in docs:

            data = doc.to_dict()

            data["id"] = doc.id

            questions.append(
                data
            )

        # recientes primero
        questions.sort(
            key=lambda q:
            q.get(
                "createdAt",
                datetime.min
            ),
            reverse=True
        )

        return questions

    def get_question_by_id(
        self,
        question_id
    ):

        doc = self.db.collection(
            "questions"
        ).document(
            question_id
        ).get()

        if not doc.exists:
            return None

        data = doc.to_dict()

        data["id"] = doc.id

        return data
        
    # ==================================
    # OPCIONAL FUTURO RANKING
    # ==================================

    def count_questions_by_user(
        self,
        user_id
    ):

        docs = (
            self.db.collection(
                "questions"
            )
            .where(
                "userId",
                "==",
                user_id
            )
            .stream()
        )

        return len(
            list(docs)
        )
