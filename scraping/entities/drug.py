from entities.detail import Detail

class Drug:
    def __init__(self, name: str, drug_type: str, link: str):
        self.name = name
        self.type = drug_type
        self.link = link
        self.details = []

    def add_detail(self, question: str, answer: str):
        self.details.append(Detail(question, answer))

    def __repr__(self):
        return f"Drug(name={self.name!r}, type={self.type!r}, link={self.link!r}, details={self.details!r}) "
