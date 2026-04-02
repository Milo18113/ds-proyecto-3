from typing import Optional
from sqlalchemy.orm import Session

from backend.domain.entities.notification import Notification
from backend.domain.repositories.notification_repository import NotificationRepository
from backend.infrastructure.orm.models.notification_model import NotificationModel


class NotificationRepositoryImpl(NotificationRepository):
    """Implementación concreta del repositorio de notificaciones usando SQLAlchemy ORM."""

    def __init__(self, db: Session):
        self.db = db

    # ── Mappers ───────────────────────────────────────────────────────────

    def _to_domain(self, model: NotificationModel) -> Notification:
        return Notification(
            id=model.id,
            recipient=model.recipient,
            channel=model.channel,
            message=model.message,
            event_type=model.event_type,
            created_at=model.created_at,
            status=model.status,
        )

    def _to_model(self, entity: Notification) -> NotificationModel:
        return NotificationModel(
            id=entity.id,
            recipient=entity.recipient,
            channel=entity.channel,
            message=entity.message,
            event_type=entity.event_type,
            status=entity.status,
            created_at=entity.created_at,
        )

    # ── CRUD ──────────────────────────────────────────────────────────────

    def save(self, notification: Notification) -> Notification:
        model = self._to_model(notification)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._to_domain(model)

    def find_by_recipient(self, user_id: str) -> list[Notification]:
        models = (
            self.db.query(NotificationModel)
            .filter(NotificationModel.recipient == user_id)
            .order_by(NotificationModel.created_at.desc())
            .all()
        )
        return [self._to_domain(m) for m in models]

    def find_all(self) -> list[Notification]:
        models = (
            self.db.query(NotificationModel)
            .order_by(NotificationModel.created_at.desc())
            .all()
        )
        return [self._to_domain(m) for m in models]

    def update(self, notification: Notification) -> Notification:
        model = (
            self.db.query(NotificationModel)
            .filter(NotificationModel.id == notification.id)
            .first()
        )
        if not model:
            raise ValueError(f"Notificación {notification.id} no encontrada.")
        model.status = notification.status
        model.message = notification.message
        self.db.commit()
        self.db.refresh(model)
        return self._to_domain(model)
