"""
Moduł widoków API dla systemu zarządzania lekami.

Zawiera endpointy do obsługi skanowania kodów leków i zarządzania powiadomieniami.
Wykorzystuje zewnętrzne API (PolishMedicinesAPI) do wyszukiwania informacji o lekach.
"""
# api/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .drug_api import PolishMedicinesAPI
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def notifications_handler(request):
    """
    Obsługuje żądania związane z ustawieniami powiadomień.

    Endpoint przyjmuje żądania POST z ustawieniami powiadomień w formacie JSON
    i aktualizuje je w bazie danych. Dla innych metod HTTP zwraca błąd.

    Args:
        request (HttpRequest): Obiekt żądania HTTP

    Returns:
        JsonResponse: Odpowiedź w formacie JSON zawierająca status operacji
            i ewentualny komunikat błędu

    Status codes:
        200: Sukces
        400: Nieprawidłowy format JSON
        405: Niedozwolona metoda HTTP
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)
            # parsowanie ustawień wysłanych przez POST request
            # ...

            # aktualizacja ustawień w db
            # ...

            return JsonResponse({
                'status': 'success',
            })
        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid JSON format'
            }, status=400)

    return JsonResponse({
        'status': 'error',
        'message': 'Method not allowed'
    }, status=405)
@api_view(['GET'])
def scan_code(request):
    """
    Endpoint do wyszukiwania leków po zeskanowanym kodzie GTIN/EAN.

    Przyjmuje kod kreskowy leku i zwraca szczegółowe informacje o leku
    pobrane z API Polskich Leków (URPL).

    Args:
        request (HttpRequest): Obiekt żądania HTTP zawierający parametr 'code'
            w query string

    Returns:
        Response: Odpowiedź REST framework zawierająca:
            - w przypadku znalezienia leku: szczegółowe informacje o leku
            - w przypadku braku leku: informację o nieznalezieniu oraz
              zeskanowany kod i jego zidentyfikowany typ

    Status codes:
        200: Sukces - lek znaleziony
        400: Brak wymaganego parametru 'code'
        404: Lek nie został znaleziony
    """
    scanned_code = request.GET.get('code')

    if not scanned_code:
        return Response({
            'error': 'Nie podano kodu'
        }, status=400)

    code_type = identify_code_type(scanned_code)

    # Wyszukiwanie w bazie URPL
    drug_data = PolishMedicinesAPI.search_drug(scanned_code)

    if drug_data and drug_data.get('content') and len(drug_data['content']) > 0:
        # Pobieramy pierwszy lek z listy content
        medicine = drug_data['content'][0]

        resp = Response({
            'found': True,
            'drug': {
                'name': medicine.get('medicinalProductName'),
                'common_name': medicine.get('commonName'),
                'power': medicine.get('medicinalProductPower'),
                'form': medicine.get('pharmaceuticalFormName'),
                'package_size': None,  # brak w odpowiedzi API
                'marketing_authorization_holder': medicine.get('subjectMedicinalProductName'),
                'marketing_authorization_number': medicine.get('registryNumber'),
                'active_substance': medicine.get('activeSubstanceName'),
                'code_info': {
                    'value': scanned_code,
                    'type': code_type
                },
                # Dodatkowe pola z API
                'atc_code': medicine.get('atcCode'),
                'expiration_date': medicine.get('expirationDateString'),
                'procedure_type': medicine.get('procedureTypeName'),
                'specimen_type': medicine.get('specimenType')
            }
        })
        print(resp)
        return resp
    else:
        return Response({
            'found': False,
            'scanned_code': scanned_code,
            'identified_type': code_type
        }, status=404)

def identify_code_type(code):
    """
    Identyfikuje typ kodu na podstawie jego formatu.

    Obecnie wszystkie kody są traktowane jako GTIN (Global Trade Item Number).
    W przyszłości funkcja może zostać rozszerzona o rozpoznawanie innych
    typów kodów.

    Args:
        code (str): Zeskanowany kod do zidentyfikowania

    Returns:
        str: Typ kodu - obecnie zawsze zwraca 'GTIN'
    """
    return 'GTIN'
