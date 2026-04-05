from backend.domain.observers.observer import Observer
from backend.domain.events.base_event import DomainEvent
from backend.domain.events.incident_events import (
    IncidentCreatedEvent,
    IncidentAssignedEvent,
    IncidentStatusChangedEvent,
)
from backend.domain.events.task_events import TaskCreatedEvent, TaskDoneEvent
from backend.domain.entities.notification import Notification


class NotificationObserver(Observer):
    """
    Observer que escucha eventos del dominio y genera notificaciones
    persistidas en la base de datos.
    """

    def __init__(self, notification_repo):
        self.notification_repo = notification_repo

    def update(self, event: DomainEvent) -> None:
        notifications = self._build_notifications(event)

        for notification in notifications:
            try:
                notification.mark_as_sent()
                self.notification_repo.save(notification)
            except Exception:
                notification.mark_as_failed()
                self.notification_repo.save(notification)

    def _build_notifications(self, event: DomainEvent) -> list[Notification]:
        notifications: list[Notification] = []

        if isinstance(event, IncidentCreatedEvent):
            incident = event.incident
            notifications.append(
                Notification(
                    id="",
                    recipient=incident.created_by,
                    channel="in_app",
                    message=f"Tu incidente '{incident.title}' fue creado correctamente.",
                    event_type=event.event_type,
                )
            )

        elif isinstance(event, IncidentAssignedEvent):
            incident = event.incident
            if event.assigned_to_id:
                notifications.append(
                    Notification(
                        id="",
                        recipient=event.assigned_to_id,
                        channel="in_app",
                        message=f"Se te asignó el incidente '{incident.title}'.",
                        event_type=event.event_type,
                    )
                )

        elif isinstance(event, IncidentStatusChangedEvent):
            incident = event.incident
            if incident.assigned_to:
                notifications.append(
                    Notification(
                        id="",
                        recipient=incident.assigned_to,
                        channel="in_app",
                        message=(
                            f"El incidente '{incident.title}' cambió de estado "
                            f"de {event.previous_status.value} a {event.new_status.value}."
                        ),
                        event_type=event.event_type,
                    )
                )

        elif isinstance(event, TaskCreatedEvent):
            task = event.task
            notifications.append(
                Notification(
                    id="",
                    recipient=task.assigned_to,
                    channel="in_app",
                    message=f"Se te asignó la tarea '{task.title}'.",
                    event_type=event.event_type,
                )
            )

        elif isinstance(event, TaskDoneEvent):
            task = event.task
            notifications.append(
                Notification(
                    id="",
                    recipient=task.assigned_to,
                    channel="in_app",
                    message=f"La tarea '{task.title}' fue marcada como completada.",
                    event_type=event.event_type,
                )
            )

        return notifications