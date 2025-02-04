"""
Moduł modeli danych dla systemu zarządzania lekami.

Definiuje struktury danych reprezentujące leki i ich kody identyfikacyjne
w bazie danych, wraz z relacjami między nimi.
"""
# models.py
from django.db import models

class Drug(models.Model):
    """
    Model reprezentujący lek w systemie.

    Przechowuje podstawowe informacje o leku, takie jak nazwa, producent,
    składniki aktywne, postać leku oraz znaczniki czasowe.

    Atrybuty:
        name (CharField): Nazwa leku (max 200 znaków)
        manufacturer (CharField): Nazwa producenta (max 200 znaków)
        active_ingredients (JSONField): Składniki aktywne i ich ilości w formacie
            {"substancja": "ilość"}
        dosage_form (CharField): Postać leku (np. tabletki, syrop) (max 100 znaków)
        created_at (DateTimeField): Data i czas utworzenia rekordu
        updated_at (DateTimeField): Data i czas ostatniej aktualizacji rekordu
    """
    name = models.CharField(max_length=200)
    manufacturer = models.CharField(max_length=200)
    active_ingredients = models.JSONField()  # Format: {"substance": "amount"}
    dosage_form = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Zwraca tekstową reprezentację obiektu leku.

        Returns:
            str: Nazwa leku wraz z producentem w nawiasach
        """
        return f"{self.name} ({self.manufacturer})"

    class Meta:
        """
        Metadane modelu Drug.

        Atrybuty:
            ordering (list): Określa domyślne sortowanie po nazwie leku
        """
        ordering = ['name']

class DrugCode(models.Model):
    """
    Model reprezentujący kody identyfikacyjne leków.

    Przechowuje różne typy kodów identyfikacyjnych przypisanych do leków,
    takie jak kody kreskowe, numery seryjne, numery partii itp.

    Atrybuty:
        CODE_TYPES (list): Lista dostępnych typów kodów w formacie (kod, opis)
        drug (ForeignKey): Relacja do modelu Drug
        code_type (CharField): Typ kodu wybrany z CODE_TYPES
        value (CharField): Wartość kodu (max 100 znaków)
        created_at (DateTimeField): Data i czas utworzenia kodu
    """
    CODE_TYPES = [
        ('BAR', 'Barcode'),
        ('SN', 'Serial Number'),
        ('LOT', 'Lot Number'),
        ('GTIN', 'Global Trade Item Number'),
        ('OTHER', 'Other')
    ]

    drug = models.ForeignKey(Drug, related_name='codes', on_delete=models.CASCADE)
    code_type = models.CharField(max_length=5, choices=CODE_TYPES)
    value = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """
        Metadane modelu DrugCode.

        Atrybuty:
            unique_together (list): Wymusza unikalność kombinacji typu kodu i jego wartości
        """
        unique_together = ['code_type', 'value']

    def __str__(self):
        """
        Zwraca tekstową reprezentację obiektu kodu leku.

        Returns:
            str: Typ kodu i jego wartość oddzielone dwukropkiem
        """
        return f"{self.code_type}: {self.value}"