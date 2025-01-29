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
    # Na testy wyłaczamy autoryzację przez tokeny
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    

    def post(self, request):
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
    # Na testy wyłaczamy autoryzację przez tokeny
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    def post(self, request):
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
    # Na testy wyłaczamy autoryzację przez tokeny
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    def post(self, request):
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
