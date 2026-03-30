from abc import ABC, abstractmethod
from backend.domain.entities.notification import Notification


class NotificationRepository(ABC):
    """
    Puerto de salida para persistencia de notificaciones.
    La implementación concreta vive en infrastructure/repositories/.
    """

    @abstractmethod
    def save(self, notification: Notification) -> None:
        """Persiste una notificación nueva o actualiza una existente."""
        ...

    @abstractmethod
    def find_by_id(self, notification_id: str) -> Notification | None:
        """Retorna una notificación por su ID, o None si no existe."""
        ...

    @abstractmethod
    def find_all(self) -> list[Notification]:
        """Retorna todas las notificaciones. Usado por Admin."""
        ...

    @abstractmethod
    def find_by_recipient(self, user_id: str) -> list[Notification]:
        """Retorna notificaciones de un usuario específico.
        Usado para la vista de Operator y Supervisor."""
        ...

    @abstractmethod
    def delete(self, notification_id: str) -> None:
        """Elimina una notificación por su ID."""
        ...