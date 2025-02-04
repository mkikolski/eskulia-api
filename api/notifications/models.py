from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class UserFCMToken(models.Model):
    """
    Model przechowujący tokeny FCM (Firebase Cloud Messaging) dla użytkowników.
    
    Model służy do zarządzania tokenami push notification dla różnych urządzeń użytkowników.
    Każdy token jest powiązany z konkretnym użytkownikiem i typem urządzenia.
    
    Attributes:
        user (ForeignKey): Powiązanie z modelem User Django
        fcm_token (str): Token FCM dla danego urządzenia
        device_type (str): Typ urządzenia (android/ios/web)
        created_at (datetime): Data i czas utworzenia tokenu
        updated_at (datetime): Data i czas ostatniej aktualizacji tokenu
        is_active (bool): Flaga określająca czy token jest aktywny
    """
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='fcm_tokens',
        verbose_name=_('User')
    )
    fcm_token = models.CharField(
        max_length=255,
        verbose_name=_('FCM Token')
    )
    device_type = models.CharField(
        max_length=50,
        choices=[
            ('android', 'Android'),
            ('ios', 'iOS'),
            ('web', 'Web'),
        ],
        verbose_name=_('Device Type')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created At')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated At')
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Is Active')
    )

    class Meta:
        """
        Metadane modelu UserFCMToken.
        
        Attributes:
            verbose_name (str): Nazwa pojedynczego obiektu w interfejsie admina
            verbose_name_plural (str): Nazwa mnogiej liczby obiektów w interfejsie admina
            unique_together (tuple): Unikalna kombinacja pól user i fcm_token
            ordering (list): Domyślne sortowanie po polu created_at malejąco
            db_table (str): Nazwa tabeli w bazie danych
        """
        verbose_name = _('User FCM Token')
        verbose_name_plural = _('User FCM Tokens')
        unique_together = ('user', 'fcm_token')
        ordering = ['-created_at']
        db_table = 'notifications_userfcmtoken'  # Dodana explicit nazwa tabeli

    def __str__(self):
        """
        Zwraca reprezentację tekstową obiektu UserFCMToken.
        
        Returns:
            str: String w formacie "nazwa_użytkownika - typ_urządzenia (pierwsze_10_znaków_tokenu)..."
        """
        return f"{self.user.username} - {self.device_type} ({self.fcm_token[:10]}...)"
