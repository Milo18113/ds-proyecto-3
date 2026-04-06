from backend.domain.commands.base_command import BaseCommand
from backend.domain.entities.notification import Notification


class SendInAppCommand(BaseCommand):
    def __init__(self, notification: Notification, provider):
        self.notification = notification
        self.provider = provider

    def execute(self) -> None:
        self.provider.send(
            recipient=self.notification.recipient,
            message=self.notification.message,
        )
