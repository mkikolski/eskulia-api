from firebase_admin import messaging
from typing import Dict, List, Any
from django.core.exceptions import ValidationError
from django.conf import settings
import firebase_admin
from firebase_admin import credentials
import logging

logger = logging.getLogger(__name__)

# Inicjalizacja Firebase Admin SDK
if not firebase_admin._apps:
    cred = credentials.Certificate(settings.FIREBASE_CONFIG)
    firebase_admin.initialize_app(cred)

class NotificationTypes:
    """
    Klasa definiująca stałe typy powiadomień w systemie.
    
    Zawiera predefiniowane typy powiadomień jako stałe klasowe oraz
    metodę pomocniczą do pobrania wszystkich dostępnych typów.
    """
    MESSAGE = 'MESSAGE'
    REMINDER = 'REMINDER'
    APPOINTMENT = 'APPOINTMENT'
    SYSTEM = 'SYSTEM'
    ALERT = 'ALERT'
    
    @classmethod
    def get_all_types(cls) -> List[str]:
        """
        Pobiera listę wszystkich zdefiniowanych typów powiadomień.

        Returns:
            List[str]: Lista zawierająca wszystkie dostępne typy powiadomień.
        """
        return [attr for attr in dir(cls) 
                if not attr.startswith('_') and 
                isinstance(getattr(cls, attr), str)]

class NotificationTemplate:
    """
    Klasa reprezentująca szablon powiadomienia.
    
    Odpowiada za formatowanie i walidację treści powiadomień według
    zdefiniowanego szablonu.

    Attributes:
        title_template (str): Szablon tytułu powiadomienia
        body_template (str): Szablon treści powiadomienia
        required_fields (List[str]): Lista wymaganych pól w treści powiadomienia
    """
    def __init__(self, title_template: str, body_template: str, required_fields: List[str]):
        """
        Inicjalizuje nowy szablon powiadomienia.

        Args:
            title_template (str): Szablon tytułu powiadomienia
            body_template (str): Szablon treści powiadomienia
            required_fields (List[str]): Lista wymaganych pól
        """
        self.title_template = title_template
        self.body_template = body_template
        self.required_fields = required_fields

    def validate_content(self, content: Dict[str, Any]) -> None:
        """
        Sprawdza, czy przekazana treść zawiera wszystkie wymagane pola.

        Args:
            content (Dict[str, Any]): Słownik z treścią powiadomienia

        Raises:
            ValidationError: Gdy brakuje wymaganych pól
        """
        missing_fields = [field for field in self.required_fields 
                         if field not in content]
        if missing_fields:
            raise ValidationError(
                f"Missing required fields: {', '.join(missing_fields)}"
            )

    def format_notification(self, content: Dict[str, Any]) -> Dict[str, str]:
        """
        Formatuje powiadomienie według szablonu.

        Args:
            content (Dict[str, Any]): Słownik z danymi do wstawienia w szablon

        Returns:
            Dict[str, str]: Sformatowane powiadomienie z tytułem i treścią

        Raises:
            ValidationError: Gdy brakuje wymaganych pól
        """
        self.validate_content(content)
        return {
            'title': self.title_template.format(**content),
            'body': self.body_template.format(**content)
        }

class NotificationService:
    """
    Serwis do zarządzania i wysyłania powiadomień FCM.
    
    Obsługuje tworzenie i wysyłanie powiadomień przy użyciu Firebase Cloud Messaging.
    Zawiera predefiniowane szablony dla różnych typów powiadomień.
    """
    def __init__(self):
        """
        Inicjalizuje serwis powiadomień z predefiniowanymi szablonami.
        """
        self.notification_templates = {
            NotificationTypes.MESSAGE: NotificationTemplate(
                title_template="Nowa wiadomość od {sender_name}",
                body_template="{message}",
                required_fields=['sender_name', 'message']
            ),
            NotificationTypes.REMINDER: NotificationTemplate(
                title_template="Przypomnienie: {title}",
                body_template="{description}",
                required_fields=['title', 'description']
            ),
            NotificationTypes.APPOINTMENT: NotificationTemplate(
                title_template="Wizyta: {appointment_type}",
                body_template="Data: {date} o {time}",
                required_fields=['appointment_type', 'date', 'time']
            ),
            NotificationTypes.SYSTEM: NotificationTemplate(
                title_template="Informacja systemowa",
                body_template="{message}",
                required_fields=['message']
            ),
            NotificationTypes.ALERT: NotificationTemplate(
                title_template="⚠️ {alert_type}",
                body_template="{message}",
                required_fields=['alert_type', 'message']
            )
        }

    def create_notification(
        self, 
        notification_type: str, 
        content: Dict[str, Any],
        token: str, 
        data: Dict[str, Any] = None
    ) -> messaging.Message:
        """
        Tworzy obiekt powiadomienia FCM na podstawie typu i treści.

        Args:
            notification_type (str): Typ powiadomienia
            content (Dict[str, Any]): Treść powiadomienia
            token (str): Token FCM urządzenia docelowego
            data (Dict[str, Any], optional): Dodatkowe dane dla powiadomienia

        Returns:
            messaging.Message: Skonfigurowany obiekt powiadomienia FCM

        Raises:
            ValidationError: Gdy podany typ powiadomienia jest nieznany
        """
        if notification_type not in self.notification_templates:
            raise ValidationError(f"Unknown notification type: {notification_type}")

        template = self.notification_templates[notification_type]
        notification_content = template.format_notification(content)

        return messaging.Message(
            notification=messaging.Notification(
                title=notification_content['title'],
                body=notification_content['body'],
            ),
            data=data or {},
            token=token,
        )

    async def send_batch_notifications(
        self, 
        notifications: List[messaging.Message]
    ) -> List[Dict]:
        """
        Wysyła serię powiadomień FCM asynchronicznie.

        Args:
            notifications (List[messaging.Message]): Lista powiadomień do wysłania

        Returns:
            List[Dict]: Lista wyników wysyłania dla każdego powiadomienia,
                       zawierająca status i identyfikator wiadomości lub błąd
        """
        results = []
        for notification in notifications:
            try:
                response = messaging.send(notification)
                results.append({
                    'status': 'success',
                    'message_id': response
                })
                logger.info(f"Notification sent successfully: {response}")
            except Exception as e:
                error_message = str(e)
                results.append({
                    'status': 'error',
                    'error': error_message
                })
                logger.error(f"Failed to send notification: {error_message}")
        return results
