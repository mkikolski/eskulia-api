class Detail:
    def __init__(self, question: str, answer: str):
        self.question = question
        self.answer = answer

    def __repr__(self):
        return f"Detail(question={self.question!r}, answer={self.answer!r})"
