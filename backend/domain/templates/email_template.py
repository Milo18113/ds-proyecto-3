from backend.domain.enums.event_type import EventType
from backend.domain.templates.notification_template import NotificationTemplate


class EmailTemplate(NotificationTemplate):
    def intro(self, event_type: EventType) -> str:
        return f"[EMAIL] Evento detectado: {event_type.value}"

    def body(self, title: str, detail: str) -> str:
        return f"Asunto: {title}\nDetalle: {detail}"