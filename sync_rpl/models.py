"""
Moduł definiujący model danych dla leków w bazie danych.

Moduł zawiera model Medicine reprezentujący produkty lecznicze wraz z ich
szczegółowymi informacjami, takimi jak nazwa, substancja czynna, opakowanie itp.
Model jest wykorzystywany do przechowywania danych z Rejestru Produktów Leczniczych.
"""
from django.db import models

class Medicine(models.Model):
    """
    Model reprezentujący produkt leczniczy w bazie danych.

    Model przechowuje szczegółowe informacje o lekach, w tym ich nazwy,
    sposób podania, moc, kod ATC i inne istotne dane farmaceutyczne.
    Wszystkie pola tekstowe oprócz identyfikatora i nazwy mogą być puste.

    Attributes:
        identifier (CharField): Unikalny identyfikator leku (max 50 znaków).
        name (CharField): Nazwa handlowa leku (max 255 znaków).
        common_name (CharField): Nazwa powszechna/międzynarodowa (max 255 znaków).
        preparation_type (CharField): Rodzaj preparatu (max 100 znaków).
        administration_route (CharField): Droga podania leku (max 255 znaków).
        strength (CharField): Moc/dawka leku (max 100 znaków).
        pharmaceutical_form (CharField): Postać farmaceutyczna (max 255 znaków).
        atc_code (CharField): Kod klasyfikacji anatomiczno-terapeutyczno-chemicznej (max 50 znaków).
        responsible_entity (CharField): Podmiot odpowiedzialny (max 255 znaków).
        active_substance (TextField): Substancja czynna/składniki aktywne.
        packaging (TextField): Informacje o dostępnych opakowaniach.

    Meta:
        db_table = 'medicines'

    Example:
        >>> lek = Medicine.objects.create(
        ...     identifier="12345",
        ...     name="Przykładowy Lek",
        ...     common_name="Substancja X",
        ...     strength="100mg"
        ... )
        >>> print(lek.name)
        'Przykładowy Lek'
    """
    identifier = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    common_name = models.CharField(max_length=255, null=True, blank=True)
    preparation_type = models.CharField(max_length=100, null=True, blank=True)
    administration_route = models.CharField(max_length=255, null=True, blank=True)
    strength = models.CharField(max_length=100, null=True, blank=True)
    pharmaceutical_form = models.CharField(max_length=255, null=True, blank=True)
    atc_code = models.CharField(max_length=50, null=True, blank=True)
    responsible_entity = models.CharField(max_length=255, null=True, blank=True)
    active_substance = models.TextField(null=True, blank=True)
    packaging = models.TextField(null=True, blank=True) 

    def __str__(self):
        """
        Zwraca reprezentację tekstową obiektu Medicine.

        Metoda używana do wyświetlania nazwy leku w interfejsie administratora
        Django i innych miejscach wymagających tekstowej reprezentacji obiektu.

        Returns:
            str: Nazwa leku.

        Example:
            >>> lek = Medicine(name="Przykładowy Lek")
            >>> str(lek)
            'Przykładowy Lek'
        """
        return self.name
