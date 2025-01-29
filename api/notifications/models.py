from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class UserFCMToken(models.Model):
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
        verbose_name = _('User FCM Token')
        verbose_name_plural = _('User FCM Tokens')
        unique_together = ('user', 'fcm_token')
        ordering = ['-created_at']
        db_table = 'notifications_userfcmtoken'  # Dodana explicit nazwa tabeli

    def __str__(self):
        return f"{self.user.username} - {self.device_type} ({self.fcm_token[:10]}...)"
