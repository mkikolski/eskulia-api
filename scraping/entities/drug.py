"""
Moduł zawierający klasę Drug reprezentującą informacje o leku.

Moduł definiuje strukturę danych do przechowywania informacji o leku,
włączając jego nazwę, typ, link oraz szczegóły w formie par pytanie-odpowiedź.
"""
from entities.detail import Detail

class Drug:
    """
    Klasa reprezentująca lek i jego szczegółowe informacje.

    Przechowuje podstawowe informacje o leku oraz kolekcję szczegółów
    w formie par pytanie-odpowiedź.

    Attributes:
        name (str): Nazwa leku
        type (str): Typ/kategoria leku
        link (str): Link do źródła informacji o leku
        details (list[Detail]): Lista obiektów Detail zawierających
            dodatkowe informacje o leku w formie pytań i odpowiedzi
    """
    def __init__(self, name: str, drug_type: str, link: str):
        """
        Inicjalizuje nowy obiekt Drug.

        Args:
            name (str): Nazwa leku
            drug_type (str): Typ/kategoria leku
            link (str): Link do źródła informacji o leku

        Example:
            >>> drug = Drug("Paracetamol", "Przeciwbólowy", "https://example.com/paracetamol")
            >>> print(drug.name)
            "Paracetamol"
        """
        self.name = name
        self.type = drug_type
        self.link = link
        self.details = []

    def add_detail(self, question: str, answer: str):
        """
        Dodaje nowy szczegół do leku w formie pary pytanie-odpowiedź.

        Tworzy nowy obiekt Detail na podstawie przekazanych parametrów
        i dodaje go do listy szczegółów leku.

        Args:
            question (str): Pytanie dotyczące leku
            answer (str): Odpowiedź na pytanie

        Example:
            >>> drug = Drug("Paracetamol", "Przeciwbólowy", "https://example.com/paracetamol")
            >>> drug.add_detail("Jak stosować?", "Doustnie, 1 tabletka co 4 godziny")
        """
        self.details.append(Detail(question, answer))

    def __repr__(self):
        """
        Zwraca reprezentację tekstową obiektu Drug.

        Metoda tworzy string reprezentujący obiekt w formie,
        która może być użyta do jego odtworzenia.

        Returns:
            str: Reprezentacja tekstowa obiektu zawierająca wszystkie
                jego atrybuty wraz z listą szczegółów

        Example:
            >>> drug = Drug("Paracetamol", "Przeciwbólowy", "https://example.com/paracetamol")
            >>> repr(drug)
            "Drug(name='Paracetamol', type='Przeciwbólowy', link='https://example.com/paracetamol', details=[])"
        """
        return f"Drug(name={self.name!r}, type={self.type!r}, link={self.link!r}, details={self.details!r}) "
