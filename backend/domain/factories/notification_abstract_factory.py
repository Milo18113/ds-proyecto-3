from abc import ABC, abstractmethod

from backend.domain.commands.base_command import BaseCommand
from backend.domain.entities.notification import Notification
from backend.domain.enums.event_type import EventType
from backend.domain.factories.entity_factory import NotificationFactory


class NotificationAbstractFactory(ABC):
    @abstractmethod
    def create_notification(
        self,
        recipient: str,
        message: str,
        event_type: EventType,
    ) -> Notification:
        ...

    @abstractmethod
    def create_send_command(self, notification: Notification, provider) -> BaseCommand:
        ...


class EmailNotificationFactory(NotificationAbstractFactory):
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

    def create_send_command(self, notification: Notification, provider) -> BaseCommand:
        from backend.domain.commands.send_email_command import SendEmailCommand
        return SendEmailCommand(notification, provider)


class InAppNotificationFactory(NotificationAbstractFactory):
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

    def create_send_command(self, notification: Notification, provider) -> BaseCommand:
        from backend.domain.commands.send_in_app_command import SendInAppCommand
        return SendInAppCommand(notification, provider)


def get_notification_factory(channel: str) -> NotificationAbstractFactory:
    factories = {
        "email": EmailNotificationFactory,
        "in_app": InAppNotificationFactory,
    }
    if channel not in factories:
        raise ValueError(f"Canal de notificación no soportado: '{channel}'")
    return factories[channel]()