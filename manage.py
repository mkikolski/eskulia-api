#!/usr/bin/env python
"""
Ten skrypt jest głównym punktem wejścia dla zarządzania projektem Django.
Umożliwia wykonywanie różnych zadań administracyjnych, takich jak:
- Uruchamianie serwera deweloperskiego
- Wykonywanie migracji bazy danych
- Tworzenie superużytkownika
- Zarządzanie statycznymi plikami
i wiele innych komend zarządzających Django.

Example:
    Przykłady użycia skryptu:
        $ python manage.py runserver
        $ python manage.py migrate
        $ python manage.py createsuperuser
"""

import os
import sys

def main():
    """
    Uruchamia zadania administracyjne Django.

    Funkcja konfiguruje środowisko Django poprzez:
    1. Ustawienie modułu ustawień Django
    2. Sprawdzenie poprawności instalacji Django
    3. Wykonanie odpowiedniej komendy administracyjnej

    Raises:
        ImportError: Gdy Django nie jest zainstalowane lub nie jest dostępne
            w ścieżce PYTHONPATH, lub gdy środowisko wirtualne nie jest aktywowane.

    Example:
        >>> main()  # Uruchomienie z linii poleceń
        # lub
        >>> if __name__ == '__main__':
        ...     main()

    Notes:
        - Upewnij się, że Django jest zainstalowane w środowisku
        - Sprawdź, czy środowisko wirtualne jest aktywowane
        - Upewnij się, że PYTHONPATH jest poprawnie skonfigurowany
    """
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eskuliaapi.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
