from abc import ABC, abstractmethod
from typing import Optional
from backend.domain.entities.notification import Notification


class NotificationRepository(ABC):
    """Puerto de salida para persistencia de notificaciones."""

    @abstractmethod
    def save(self, notification: Notification) -> Notification:
        ...

    @abstractmethod
    def find_by_recipient(self, user_id: str) -> list[Notification]:
        ...

    @abstractmethod
    def find_all(self) -> list[Notification]:
        ...

    @abstractmethod
    def update(self, notification: Notification) -> Notification:
        ...
