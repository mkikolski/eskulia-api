from rest_framework import serializers
from .models import UserFCMToken

class UserFCMTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFCMToken
        fields = ['id', 'fcm_token', 'device_type', 'is_active']
        read_only_fields = ['id']

class NotificationRequestSerializer(serializers.Serializer):
    recipients = serializers.ListField(
        child=serializers.IntegerField(),
        help_text="Lista ID użytkowników"
    )
    notification_type = serializers.CharField(
        help_text="Typ powiadomienia"
    )
    content = serializers.DictField(
        help_text="Zawartość powiadomienia"
    )
    additional_data = serializers.DictField(
        required=False,
        help_text="Dodatkowe dane dla powiadomienia"
    )

class FCMTokenUpdateSerializer(serializers.Serializer):
    fcm_token = serializers.CharField(
        max_length=255,
        help_text="Token FCM urządzenia"
    )
    device_type = serializers.ChoiceField(
        choices=['android', 'ios', 'web'],
        help_text="Typ urządzenia"
    )
