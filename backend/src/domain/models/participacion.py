class Participacion:

    def __init__(self, user_id, question_count=0):
        self.user_id = user_id
        self.question_count = question_count

    def to_dict(self):
        return {
            "userId": self.user_id,
            "questionCount": self.question_count
        }
