class Retroalimentacion:

    def __init__(self, feedback, improved_question):
        self.feedback = feedback
        self.improved_question = improved_question

    def to_dict(self):
        return {
            "feedback": self.feedback,
            "improvedQuestion": self.improved_question
        }
