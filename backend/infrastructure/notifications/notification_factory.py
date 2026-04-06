from backend.infrastructure.notifications.email_provider import EmailProvider
from backend.infrastructure.notifications.in_app_provider import InAppProvider


class NotificationProviderFactory:
    @staticmethod
    def create(channel: str):
        if channel == "email":
            return EmailProvider()
        if channel == "in_app":
            return InAppProvider()
        raise ValueError(f"Canal no soportado: {channel}")