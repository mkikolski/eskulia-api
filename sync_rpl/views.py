"""
Moduł zawierający widoki API dla operacji na lekach.

Moduł dostarcza endpointy REST API do wyszukiwania leków po nazwie,
kodzie kreskowym oraz do aktualizacji bazy danych leków.
Wykorzystuje Django REST Framework do obsługi żądań HTTP.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.contrib.postgres.search import TrigramSimilarity
from .models import Medicine
from .serializers import MedicineSerializer
from .database_update_django import main

class MedicineByNameView(APIView):
    """
    Widok API do wyszukiwania leków po nazwie.

    Wykorzystuje algorytm podobieństwa trigramów do wyszukiwania przybliżonych
    dopasowań nazw leków. Zwraca listę leków posortowaną według stopnia
    podobieństwa do szukanej frazy.

    Endpoints:
        GET /api/medicines/name/{name}/: Wyszukuje leki o nazwie podobnej do podanej.

    Attributes:
        threshold (float): Próg podobieństwa dla wyników wyszukiwania (0.3).
    """
    def get(self, request, name):
        """
        Obsługuje żądanie GET do wyszukiwania leków po nazwie.

        Metoda wyszukuje leki, których nazwa jest podobna do podanej,
        używając algorytmu podobieństwa trigramów PostgreSQL.

        Args:
            request: Obiekt żądania HTTP.
            name (str): Nazwa leku do wyszukania.

        Returns:
            Response: Odpowiedź HTTP zawierająca znalezione leki lub komunikat o błędzie.
                Status 200: Lista znalezionych leków
                Status 404: Gdy nie znaleziono pasujących leków
                Status 500: W przypadku błędu serwera

        Example:
            >>> response = client.get('/api/medicines/name/Apap')
            >>> print(response.status_code)
            200
        """
        try:
            medicines = Medicine.objects.annotate(similarity=TrigramSimilarity('name', name)) \
                .filter(similarity__gt=0.3) \
                .order_by('-similarity')

            if not medicines.exists():
                return Response({"error": "Nie znaleziono leku o podanej nazwie."}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = MedicineSerializer(medicines, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MedicineByBarcodeView(APIView):
    """
    Widok API do wyszukiwania leków po kodzie kreskowym.

    Umożliwia wyszukiwanie leków na podstawie kodu kreskowego opakowania.
    Zwraca szczegółowe informacje o znalezionym leku wraz z informacjami
    o konkretnym opakowaniu.

    Endpoints:
        GET /api/medicines/barcode/{barcode}/: Wyszukuje lek po kodzie kreskowym.
    """
    def get(self, request, barcode):
        """
        Obsługuje żądanie GET do wyszukiwania leków po kodzie kreskowym.

        Metoda wyszukuje lek na podstawie kodu kreskowego i zwraca
        szczegółowe informacje o znalezionym produkcie oraz jego opakowaniu.

        Args:
            request: Obiekt żądania HTTP.
            barcode (str): Kod kreskowy do wyszukania.

        Returns:
            Response: Odpowiedź HTTP zawierająca dane znalezionego leku lub komunikat o błędzie.
                Status 200: Szczegóły znalezionego leku
                Status 404: Gdy nie znaleziono leku lub opakowania
                Status 500: W przypadku błędu serwera

        Example:
            >>> response = client.get('/api/medicines/barcode/5909990239924')
            >>> print(response.status_code)
            200
        """
        try:
            medicine = Medicine.objects.filter(packaging__icontains=barcode).first()

            if not medicine:
                return Response({"error": "Nie znaleziono leku z podanym kodem kreskowym."}, status=status.HTTP_404_NOT_FOUND)

            packaging_details = next(
                (line for line in medicine.packaging.split("\n") if barcode in line), None
            )

            if not packaging_details:
                return Response({"error": "Kod kreskowy nie pasuje do żadnego opakowania."}, status=status.HTTP_404_NOT_FOUND)

            response_data = {
                "name": medicine.name,
                "common_name": medicine.common_name,
                "strength": medicine.strength,
                "pharmaceutical_form": medicine.pharmaceutical_form,
                "packaging_details": packaging_details,
                "active_substance": medicine.active_substance,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FetchMedicines(APIView):
    """
    Widok API do aktualizacji bazy danych leków.

    Inicjuje proces pobierania i aktualizacji danych o lekach
    z zewnętrznego źródła (Rejestru Produktów Leczniczych).

    Endpoints:
        GET /api/medicines/update/: Uruchamia proces aktualizacji bazy danych.
    """
    def get(self, request):
        """
        Obsługuje żądanie GET do aktualizacji bazy danych leków.

        Metoda wywołuje funkcję main() z modułu database_update_django,
        która pobiera najnowsze dane o lekach i aktualizuje bazę danych.

        Args:
            request: Obiekt żądania HTTP.

        Returns:
            Response: Odpowiedź HTTP informująca o statusie operacji.
                Status 200: Aktualizacja zakończona powodzeniem

        Example:
            >>> response = client.get('/api/medicines/update/')
            >>> print(response.status_code)
            200
        """
        main()
        return Response(status=status.HTTP_200_OK)