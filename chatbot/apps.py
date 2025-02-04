"""
Moduł konfiguracyjny aplikacji Django 'chatbot'.

Zawiera podstawową konfigurację aplikacji chatbot, w tym ustawienia
auto-field dla modeli oraz nazwę aplikacji.
"""
from django.apps import AppConfig


class ChatbotConfig(AppConfig):
    """
    Klasa konfiguracyjna dla aplikacji chatbot.
    
    Definiuje podstawowe ustawienia aplikacji Django, takie jak
    typ automatycznego pola ID dla modeli oraz nazwę aplikacji.

    Attributes:
        default_auto_field (str): Określa typ pola używanego jako
            automatyczny identyfikator w modelach. Ustawiony na
            'django.db.models.BigAutoField' dla obsługi dużych
            liczb całkowitych jako ID.
        name (str): Nazwa aplikacji Django używana do jej
            identyfikacji w projekcie.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chatbot'
