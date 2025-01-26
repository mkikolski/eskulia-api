# API Powiadomień FCM

## Spis treści

1. [Wprowadzenie](#wprowadzenie)
2. [Konfiguracja](#konfiguracja)
3. [Endpointy](#endpointy)
   - [Wysyłanie powiadomień](#wysyłanie-powiadomień)
   - [Aktualizacja tokenu FCM](#aktualizacja-tokenu-fcm)
   - [Usunięcie tokenu FCM](#usunięcie-tokenu-fcm)
4. [Modele](#modele)
5. [Uwagi implementacyjne](#uwagi-implementacyjne)

## Wprowadzenie

API służy do zarządzania powiadomieniami Firebase Cloud Messaging (FCM) w aplikacji Django. Umożliwia:
- Wysyłanie powiadomień do wybranych użytkowników
- Zarządzanie tokenami FCM (dodawanie/aktualizacja/usuwanie)
- Obsługę różnych typów urządzeń (Android, iOS, Web)

## Konfiguracja

### Wymagane zależności
```python
# requirements.txt
djangorestframework
firebase-admin  # do obsługi FCM
```

### Struktura projektu
```
notifications/
├── models.py
├── serializers.py
├── urls.py
└── views.py
```

## Endpointy

### Wysyłanie powiadomień

**Endpoint**: `POST /notifications/send/`

Wysyła powiadomienia FCM do określonych użytkowników.

#### Request
```json
{
    "recipients": [1, 2, 3],
    "notification_type": "TYPE",
    "content": {
        "title": "Tytuł powiadomienia",
        "body": "Treść powiadomienia"
    },
    "additional_data": {
        "key1": "value1",
        "key2": "value2"
    }
}
```

| Parametr | Typ | Wymagane | Opis |
|----------|-----|----------|------|
| recipients | array[int] | Tak | Lista ID użytkowników |
| notification_type | string | Tak | Typ powiadomienia |
| content | object | Tak | Zawartość powiadomienia |
| additional_data | object | Nie | Dodatkowe dane |

#### Response

**200 OK**
```json
{
    "success": true,
    "results": [
        // Wyniki wysyłania powiadomień
    ]
}
```

**400 Bad Request**
```json
{
    "error": "Opis błędu"
}
```

### Aktualizacja tokenu FCM

**Endpoint**: `POST /notifications/token/update/`

Aktualizuje lub tworzy nowy token FCM dla użytkownika.

#### Request
```json
{
    "fcm_token": "example_fcm_token_string",
    "device_type": "android"
}
```

| Parametr | Typ | Wymagane | Opis |
|----------|-----|----------|------|
| fcm_token | string | Tak | Token FCM (max 255 znaków) |
| device_type | string | Tak | Typ urządzenia: 'android', 'ios' lub 'web' |

#### Response

**200 OK**
```json
{
    "id": 1,
    "fcm_token": "example_fcm_token_string",
    "device_type": "android",
    "is_active": true
}
```

### Usunięcie tokenu FCM

**Endpoint**: `POST /notifications/token/delete/`

Dezaktywuje token FCM dla użytkownika.

## Modele

### UserFCMToken

```python
class UserFCMToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fcm_token = models.CharField(max_length=255)
    device_type = models.CharField(
        max_length=50,
        choices=[
            ('android', 'Android'),
            ('ios', 'iOS'),
            ('web', 'Web'),
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'fcm_token')
        ordering = ['-created_at']
```

## Uwagi implementacyjne

1. **Autoryzacja**
   - Obecnie wyłączona do celów testowych (`permission_classes = [AllowAny]`)
   - Docelowo będzie wymagana (`IsAuthenticated`)

2. **Tokeny FCM**
   - Unikalność: Kombinacja user-token musi być unikalna
   - Automatyczne timestampy dla created_at i updated_at
   - Domyślnie aktywne (is_active=True)

3. **Obsługiwane typy urządzeń**
   - Android
   - iOS
   - Web

4. **Ograniczenia**
   - Maksymalna długość tokena FCM: 255 znaków
   - Wymagane pola przy aktualizacji: fcm_token i device_type

## Przykłady użycia

### Wysłanie powiadomienia
```bash
curl -X POST http://your-api/notifications/send/ \
-H "Content-Type: application/json" \
-d '{
    "recipients": [1, 2],
    "notification_type": "MESSAGE",
    "content": {
        "title": "Nowa wiadomość",
        "body": "Masz nową wiadomość od użytkownika"
    }
}'
```

### Aktualizacja tokenu
```bash
curl -X POST http://your-api/notifications/token/update/ \
-H "Content-Type: application/json" \
-d '{
    "fcm_token": "example_token",
    "device_type": "android"
}'
```

### Usunięcie tokenu
```bash
curl -X POST http://your-api/notifications/token/delete/
```

## Status kodów HTTP

| Kod | Opis |
|-----|------|
| 200 | Sukces |
| 400 | Błędne żądanie (np. brak wymaganych pól) |
| 401 | Brak autoryzacji |
| 404 | Nie znaleziono (np. brak aktywnych tokenów) |
| 500 | Błąd serwera |

## Bezpieczeństwo

1. **Autoryzacja**
   - Docelowo wszystkie endpointy będą wymagać autoryzacji
   - Tokeny są powiązane z konkretnym użytkownikiem

2. **Walidacja**
   - Sprawdzanie poprawności tokenów FCM
   - Walidacja typów urządzeń
   - Weryfikacja istnienia użytkowników

3. **Ograniczenia**
   - Jeden użytkownik może mieć wiele tokenów
   - Tokeny mogą być dezaktywowane, ale nie są usuwane z bazy

## Przyszłe rozszerzenia

1. Dodanie obsługi grup użytkowników
2. Implementacja kolejkowania powiadomień
3. Dodanie statystyk dostarczenia
4. Rozszerzenie typów powiadomień