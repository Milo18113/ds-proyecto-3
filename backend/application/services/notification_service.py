from backend.domain.enums.event_type import EventType
from backend.domain.events.incident_events import (
    IncidentCreatedEvent,
    IncidentAssignedEvent,
    IncidentStatusChangedEvent,
)
from backend.domain.events.task_events import TaskCreatedEvent, TaskDoneEvent
from backend.domain.factories.notification_abstract_factory import get_notification_factory
from backend.domain.repositories.notification_repository import NotificationRepository
from backend.domain.templates.email_template import EmailTemplate
from backend.domain.templates.in_app_template import InAppTemplate
from backend.infrastructure.notifications.notification_factory import NotificationProviderFactory


class NotificationService:
    """
    Coordina la creación, envío y actualización de notificaciones.
    """

    def __init__(self, notification_repo: NotificationRepository):
        self.notification_repo = notification_repo
        self.templates = {
            "email": EmailTemplate(),
            "in_app": InAppTemplate(),
        }

    def handle_event(self, event) -> None:
        recipient, title, detail = self._extract_payload(event)

        for channel in ("email", "in_app"):
            template = self.templates[channel]
            message = template.build_message(event.event_type, title, detail)

            abstract_factory = get_notification_factory(channel)
            provider = NotificationProviderFactory.create(channel)

            notification = abstract_factory.create_notification(
                recipient=recipient,
                message=message,
                event_type=event.event_type,
            )

            saved = self.notification_repo.save(notification)
            command = abstract_factory.create_send_command(saved, provider)

            try:
                command.execute()
                saved.mark_as_sent()
            except Exception:
                saved.mark_as_failed()

            self.notification_repo.update(saved)

    def _extract_payload(self, event):
        if isinstance(event, IncidentCreatedEvent):
            return (
                event.incident.created_by,
                event.incident.title,
                f"Incidente creado con severidad {event.incident.severity.value}",
            )

        if isinstance(event, IncidentAssignedEvent):
            return (
                event.assigned_to_id,
                event.incident.title,
                f"Se te asignó un incidente.",
            )

        if isinstance(event, IncidentStatusChangedEvent):
            recipient = event.incident.assigned_to or event.incident.created_by
            return (
                recipient,
                event.incident.title,
                f"Estado cambiado de {event.previous_status.value} a {event.new_status.value}",
            )

        if isinstance(event, TaskCreatedEvent):
            return (
                event.task.assigned_to,
                event.task.title,
                f"Tienes una nueva tarea del incidente {event.task.incident_id}",
            )

        if isinstance(event, TaskDoneEvent):
            return (
                event.task.assigned_to,
                event.task.title,
                "La tarea fue marcada como DONE.",
            )

        raise ValueError(f"Evento no soportado por NotificationService: {type(event).__name__}")