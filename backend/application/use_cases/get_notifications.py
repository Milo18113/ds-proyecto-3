from backend.domain.repositories.notification_repository import NotificationRepository
from backend.domain.entities.user import User
from backend.application.dtos.notification_dto import NotificationResponseDTO


class GetNotificationsUseCase:
    """
    Caso de uso: consultar notificaciones según el rol del usuario.
    - OPERATOR / SUPERVISOR: solo sus notificaciones.
    - ADMIN: todas las notificaciones.
    """

    def __init__(self, notification_repo: NotificationRepository):
        self.notification_repo = notification_repo

    def execute(self, current_user: User) -> list[NotificationResponseDTO]:
        if current_user.can_view_all_notifications():
            notifications = self.notification_repo.find_all()
        else:
            notifications = self.notification_repo.find_by_recipient(current_user.id)

        return [
            NotificationResponseDTO(
                id=n.id,
                recipient=n.recipient,
                channel=n.channel,
                message=n.message,
                event_type=n.event_type,
                status=n.status,
                created_at=n.created_at,
            )
            for n in notifications
        ]
