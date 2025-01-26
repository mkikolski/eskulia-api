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
