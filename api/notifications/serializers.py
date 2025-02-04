from rest_framework import serializers
from .models import UserFCMToken

class UserFCMTokenSerializer(serializers.ModelSerializer):
    """
    Serializer dla modelu UserFCMToken.
    
    Służy do serializacji i deserializacji obiektów UserFCMToken w API.
    Zawiera podstawowe pola modelu z wyłączeniem pól związanych z czasem
    i relacją z użytkownikiem.
    """
    class Meta:
        """
        Konfiguracja serializera UserFCMToken.

        Attributes:
            model: Model, którego dotyczy serializer
            fields: Lista pól, które mają być serializowane
            read_only_fields: Lista pól tylko do odczytu
        """
        model = UserFCMToken
        fields = ['id', 'fcm_token', 'device_type', 'is_active']
        read_only_fields = ['id']

class NotificationRequestSerializer(serializers.Serializer):
    """
    Serializer do obsługi żądań wysyłania powiadomień.
    
    Używany do walidacji i strukturyzacji danych wejściowych przy wysyłaniu
    powiadomień do wielu użytkowników jednocześnie.

    Attributes:
        recipients (List[int]): Lista identyfikatorów użytkowników, do których ma być wysłane powiadomienie
        notification_type (str): Określa typ wysyłanego powiadomienia
        content (dict): Zawartość powiadomienia w formie słownika
        additional_data (dict, optional): Opcjonalne dodatkowe dane związane z powiadomieniem
    """
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
    """
    Serializer do aktualizacji tokenów FCM.
    
    Służy do walidacji i przetwarzania żądań aktualizacji lub dodawania
    nowych tokenów FCM dla urządzeń użytkowników.

    Attributes:
        fcm_token (str): Token FCM przypisany do konkretnego urządzenia
        device_type (str): Typ urządzenia (android/ios/web)
    """
    fcm_token = serializers.CharField(
        max_length=255,
        help_text="Token FCM urządzenia"
    )
    device_type = serializers.ChoiceField(
        choices=['android', 'ios', 'web'],
        help_text="Typ urządzenia"
    )
