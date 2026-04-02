from abc import ABC, abstractmethod

from backend.domain.commands.base_command import BaseCommand
from backend.domain.entities.notification import Notification
from backend.domain.enums.event_type import EventType
from backend.domain.factories.entity_factory import NotificationFactory


class NotificationAbstractFactory(ABC):
    """
    Abstract Factory para el módulo de notificaciones.

    Agrupa la creación de:
      - Notification (entidad de dominio)
      - Command (para ejecutar el envío)

    Cada fábrica concreta corresponde a un canal (email, in-app),
    garantizando consistencia entre la notificación y su comando de envío.

    Justificación:
      Se eligió Abstract Factory porque el sistema maneja múltiples canales
      de notificación (email e in-app), y cada canal requiere crear dos
      objetos relacionados: la entidad Notification y el Command que ejecuta
      el envío. Usar Abstract Factory asegura que ambos objetos pertenezcan
      al mismo canal sin riesgo de mezclar, por ejemplo, una notificación
      de tipo email con un comando de envío in-app.
    """

    @abstractmethod
    def create_notification(
        self,
        recipient: str,
        message: str,
        event_type: EventType,
    ) -> Notification:
        """Crea la entidad Notification para el canal concreto."""
        ...

    @abstractmethod
    def create_send_command(self, notification: Notification) -> BaseCommand:
        """Crea el Command de envío apropiado para el canal concreto."""
        ...


class EmailNotificationFactory(NotificationAbstractFactory):
    """
    Fábrica concreta para el canal email.
    Crea Notification con channel='email' y SendEmailCommand.
    """

    def create_notification(
        self,
        recipient: str,
        message: str,
        event_type: EventType,
    ) -> Notification:
        return NotificationFactory.create(
            recipient=recipient,
            channel="email",
            message=message,
            event_type=event_type,
        )

    def create_send_command(self, notification: Notification) -> BaseCommand:
        from backend.domain.commands.send_email_command import SendEmailCommand
        return SendEmailCommand(notification)


class InAppNotificationFactory(NotificationAbstractFactory):
    """
    Fábrica concreta para el canal in-app.
    Crea Notification con channel='in_app' y SendInAppCommand.
    """

    def create_notification(
        self,
        recipient: str,
        message: str,
        event_type: EventType,
    ) -> Notification:
        return NotificationFactory.create(
            recipient=recipient,
            channel="in_app",
            message=message,
            event_type=event_type,
        )

    def create_send_command(self, notification: Notification) -> BaseCommand:
        from backend.domain.commands.send_in_app_command import SendInAppCommand
        return SendInAppCommand(notification)


def get_notification_factory(channel: str) -> NotificationAbstractFactory:
    """Retorna la fábrica concreta según el canal solicitado."""
    factories = {
        "email": EmailNotificationFactory,
        "in_app": InAppNotificationFactory,
    }
    if channel not in factories:
        raise ValueError(f"Canal de notificación no soportado: '{channel}'")
    return factories[channel]()
