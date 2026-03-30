from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4
from backend.domain.enums.event_type import EventType
from backend.domain.enums.notification_status import NotificationStatus


@dataclass
class Notification:
    """
    Entidad de dominio que representa una notificación generada
    automáticamente por un evento del sistema.
    Su construcción y envío se delegan al patrón Command y Template Method
    en backend/domain/commands/ y backend/domain/templates/.
    """
    id: str
    recipient: str                       # ID del usuario destinatario
    channel: str                         # "email" | "in_app"
    message: str
    event_type: EventType
    created_at: datetime = field(default_factory=datetime.utcnow)
    status: NotificationStatus = field(default=NotificationStatus.PENDING)

    def __post_init__(self):
        if not self.id:
            self.id = str(uuid4())
        self._validate()

    def _validate(self):
        if not self.recipient or not self.recipient.strip():
            raise ValueError("La notificación debe tener un destinatario.")
        if not self.message or not self.message.strip():
            raise ValueError("El mensaje de la notificación no puede estar vacío.")
        if self.channel not in ("email", "in_app"):
            raise ValueError(f"Canal inválido: '{self.channel}'. Use 'email' o 'in_app'.")
        if not isinstance(self.event_type, EventType):
            raise ValueError(f"Tipo de evento inválido: {self.event_type}")

    def mark_as_sent(self) -> None:
        self.status = NotificationStatus.SENT

    def mark_as_failed(self) -> None:
        self.status = NotificationStatus.FAILED

    def is_pending(self) -> bool:
        return self.status == NotificationStatus.PENDING

    def __repr__(self) -> str:
        return (
            f"<Notification id={self.id} recipient={self.recipient} "
            f"channel={self.channel} event={self.event_type} status={self.status}>"
        )
