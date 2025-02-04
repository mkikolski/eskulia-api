"""
Moduł zawierający klasę Detail reprezentującą parę pytanie-odpowiedź.

Klasa służy do przechowywania i reprezentacji pojedynczego pytania
wraz z odpowiadającą mu odpowiedzią.
"""
class Detail:
    """
    Klasa reprezentująca szczegóły w formie pary pytanie-odpowiedź.

    Przechowuje pojedyncze pytanie i odpowiadającą mu odpowiedź,
    umożliwiając ich łatwe przechowywanie i reprezentację tekstową.

    Attributes:
        question (str): Treść pytania
        answer (str): Treść odpowiedzi
    """
    def __init__(self, question: str, answer: str):
        """
        Inicjalizuje nowy obiekt Detail.

        Args:
            question (str): Pytanie do zapisania
            answer (str): Odpowiedź na pytanie

        Example:
            >>> detail = Detail("Jak się masz?", "Dziękuję, dobrze!")
            >>> print(detail.question)
        """
        self.question = question
        self.answer = answer

    def __repr__(self):
        """
        Zwraca reprezentację tekstową obiektu Detail.

        Metoda tworzy string reprezentujący obiekt w formie,
        która może być użyta do jego odtworzenia.

        Returns:
            str: Reprezentacja tekstowa obiektu w formacie:
                "Detail(question='pytanie', answer='odpowiedź')"

        Example:
            >>> detail = Detail("Pytanie", "Odpowiedź")
            >>> repr(detail)
            "Detail(question='Pytanie', answer='Odpowiedź')"
        """
        return f"Detail(question={self.question!r}, answer={self.answer!r})"
