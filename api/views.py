# api/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .drug_api import PolishMedicinesAPI
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def notifications_handler(request):
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
    Endpoint do wyszukiwania leków po zeskanowanym kodzie GTIN/EAN
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
    Na razie wszystkie kody traktujemy jako GTIN
    """
    return 'GTIN'
