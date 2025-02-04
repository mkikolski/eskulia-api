"""
Moduł konfiguracyjny dla aplikacji Django 'sync_rpl'.

Moduł zawiera konfigurację aplikacji Django odpowiedzialnej za synchronizację
danych z Rejestrem Produktów Leczniczych (RPL).
"""
from django.apps import AppConfig

class SyncRplConfig(AppConfig):
    """
    Klasa konfiguracyjna dla aplikacji sync_rpl.

    Klasa dziedziczy po django.apps.AppConfig i definiuje podstawowe
    ustawienia dla aplikacji Django odpowiedzialnej za synchronizację
    danych z Rejestrem Produktów Leczniczych.

    Attributes:
        name (str): Nazwa aplikacji Django używana w ustawieniach projektu.
            Wartość 'sync_rpl' jest używana do identyfikacji aplikacji
            w ramach projektu Django.

    Example:
        W pliku settings.py projektu Django:
        >>> INSTALLED_APPS = [
        ...     'sync_rpl.apps.SyncRplConfig',
        ...     # inne aplikacje
        ... ]
    """
    name = 'sync_rpl'  
