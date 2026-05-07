class Pregunta:

    def __init__(
        self,
        course_id,
        course_name,
        user_id,
        user_name,
        question_text,
        ai_level=None,
        ai_feedback=None,
        improved_question=None
    ):
        self.course_id = course_id
        self.course_name = course_name
        self.user_id = user_id
        self.user_name = user_name
        self.question_text = question_text
        self.ai_level = ai_level
        self.ai_feedback = ai_feedback
        self.improved_question = improved_question

    def to_dict(self):
        return {
            "courseId": self.course_id,
            "courseName": self.course_name,
            "userId": self.user_id,
            "userName": self.user_name,
            "questionText": self.question_text,
            "aiLevel": self.ai_level,
            "aiFeedback": self.ai_feedback,
            "improvedQuestion": self.improved_question
        }
