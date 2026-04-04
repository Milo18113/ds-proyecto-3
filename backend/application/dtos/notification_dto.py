from pydantic import BaseModel
from datetime import datetime

from backend.domain.enums.event_type import EventType
from backend.domain.enums.notification_status import NotificationStatus


class NotificationResponseDTO(BaseModel):
    """DTO de respuesta para una notificación."""
    id: str
    recipient: str
    channel: str
    message: str
    event_type: EventType
    status: NotificationStatus
    created_at: datetime

    class Config:
        from_attributes = True
