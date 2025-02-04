"""
Moduł konfiguracyjny dla aplikacji API Django.

Ten moduł zawiera podstawową konfigurację aplikacji API,
definiując jej nazwę oraz typ domyślnego pola automatycznej
numeracji (auto field).
"""
from django.apps import AppConfig


class ApiConfig(AppConfig):
    """
    Klasa konfiguracyjna dla aplikacji API.

    Definiuje podstawowe ustawienia aplikacji Django, w tym:
    - typ pola automatycznej numeracji
    - nazwę aplikacji

    Atrybuty:
        default_auto_field (str): Określa typ pola używanego do automatycznej
            numeracji w modelach (BigAutoField)
        name (str): Nazwa aplikacji w projekcie Django
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
