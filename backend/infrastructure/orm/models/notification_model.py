from sqlalchemy import Column, String, DateTime, ForeignKey, Enum as SAEnum
from datetime import datetime

from backend.infrastructure.orm.base import Base
from backend.domain.enums.event_type import EventType
from backend.domain.enums.notification_status import NotificationStatus


class NotificationModel(Base):
    """Modelo ORM para la tabla notifications."""
    __tablename__ = "notifications"

    id = Column(String, primary_key=True)
    recipient = Column(String, ForeignKey("users.id"), nullable=False)
    channel = Column(String, nullable=False)  # "email" | "in_app"
    message = Column(String, nullable=False)
    event_type = Column(
        SAEnum(EventType, name="event_type_enum", create_constraint=True),
        nullable=False,
    )
    status = Column(
        SAEnum(NotificationStatus, name="notification_status_enum", create_constraint=True),
        nullable=False,
        default=NotificationStatus.PENDING,
    )
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
