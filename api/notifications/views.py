"""
Moduł widoków API dla systemu powiadomień FCM.

Zawiera widoki do obsługi wysyłania powiadomień oraz zarządzania tokenami FCM
dla użytkowników aplikacji.
"""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q
import asyncio

from .models import UserFCMToken
from .serializers import (
    NotificationRequestSerializer,
    FCMTokenUpdateSerializer,
    UserFCMTokenSerializer
)
from .services import NotificationService, NotificationTypes

class SendNotificationView(APIView):
    """
    Widok API do wysyłania powiadomień FCM do użytkowników.

    Obsługuje wysyłanie powiadomień push do określonych użytkowników
    za pomocą Firebase Cloud Messaging (FCM).

    Atrybuty:
        permission_classes: Określa uprawnienia dostępu do widoku
            (obecnie AllowAny dla celów testowych)

    Metody:
        post: Przetwarza żądanie wysłania powiadomień
    """
    # Na testy wyłaczamy autoryzację przez tokeny
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    

    def post(self, request):
        """
        Obsługuje żądanie POST do wysyłania powiadomień.

        Args:
            request: Obiekt żądania HTTP zawierający dane powiadomienia

        Returns:
            Response: Odpowiedź HTTP z wynikiem operacji wysyłania

        Raises:
            400 Bad Request: Gdy dane są nieprawidłowe lub typ powiadomienia jest nieznany
            404 Not Found: Gdy nie znaleziono aktywnych tokenów FCM dla odbiorców
        """
        serializer = NotificationRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        data = serializer.validated_data

        if data['notification_type'] not in NotificationTypes.get_all_types():
            return Response({
                'error': f"Invalid notification type. Available types: "
                        f"{', '.join(NotificationTypes.get_all_types())}"
            }, status=status.HTTP_400_BAD_REQUEST)

        tokens = UserFCMToken.objects.filter(
            Q(user_id__in=data['recipients']) & 
            Q(is_active=True)
        ).values_list('user_id', 'fcm_token')

        if not tokens:
            return Response({
                'error': "No active FCM tokens found for specified recipients"
            }, status=status.HTTP_404_NOT_FOUND)

        notification_service = NotificationService()
        notifications = []

        for user_id, token in tokens:
            try:
                notification = notification_service.create_notification(
                    notification_type=data['notification_type'],
                    content=data['content'],
                    token=token,
                    data={
                        'type': data['notification_type'],
                        'user_id': str(user_id),
                        **data.get('additional_data', {})
                    }
                )
                notifications.append(notification)
            except Exception as e:
                return Response({
                    'error': f"Error creating notification: {str(e)}"
                }, status=status.HTTP_400_BAD_REQUEST)

        results = asyncio.run(
            notification_service.send_batch_notifications(notifications)
        )

        return Response({
            'success': True,
            'results': results
        }, status=status.HTTP_200_OK)

class UpdateFCMTokenView(APIView):
    """
    Widok API do aktualizacji tokenu FCM dla użytkownika.

    Pozwala na aktualizację lub utworzenie nowego tokenu FCM
    dla urządzenia użytkownika.

    Atrybuty:
        permission_classes: Określa uprawnienia dostępu do widoku
            (obecnie AllowAny dla celów testowych)

    Metody:
        post: Przetwarza żądanie aktualizacji tokenu FCM
    """
    # Na testy wyłaczamy autoryzację przez tokeny
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Obsługuje żądanie POST do aktualizacji tokenu FCM.

        Args:
            request: Obiekt żądania HTTP zawierający nowy token FCM

        Returns:
            Response: Odpowiedź HTTP z zaktualizowanym tokenem

        Raises:
            400 Bad Request: Gdy dane są nieprawidłowe
        """
        serializer = FCMTokenUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        token_data = serializer.validated_data
        
        token, created = UserFCMToken.objects.update_or_create(
            user=request.user,
            fcm_token=token_data['fcm_token'],
            defaults={
                'device_type': token_data['device_type'],
                'is_active': True
            }
        )

        return Response(
            UserFCMTokenSerializer(token).data,
            status=status.HTTP_200_OK
        )

class DeleteFCMTokenView(APIView):
    """
    Widok API do dezaktywacji tokenu FCM.

    Pozwala na oznaczenie tokenu FCM jako nieaktywnego,
    co skutkuje zaprzestaniem wysyłania powiadomień na dane urządzenie.

    Atrybuty:
        permission_classes: Określa uprawnienia dostępu do widoku
            (obecnie AllowAny dla celów testowych)

    Metody:
        post: Przetwarza żądanie dezaktywacji tokenu FCM
    """

    # Na testy wyłaczamy autoryzację przez tokeny
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Obsługuje żądanie POST do dezaktywacji tokenu FCM.

        Args:
            request: Obiekt żądania HTTP zawierający token FCM do dezaktywacji

        Returns:
            Response: Odpowiedź HTTP z potwierdzeniem dezaktywacji

        Raises:
            400 Bad Request: Gdy nie podano tokenu FCM
            404 Not Found: Gdy nie znaleziono tokenu dla użytkownika
        """
        fcm_token = request.data.get('fcm_token')
        if not fcm_token:
            return Response({
                'error': 'FCM token is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = UserFCMToken.objects.get(
                user=request.user,
                fcm_token=fcm_token
            )
            token.is_active = False
            token.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except UserFCMToken.DoesNotExist:
            return Response({
                'error': 'Token not found'
            }, status=status.HTTP_404_NOT_FOUND)
