from backend.domain.events.base_event import DomainEvent
from backend.domain.observers.observer import Observer


class NotificationObserver(Observer):
    """
    Observer concreto que delega la generación de notificaciones
    al NotificationService.
    """

    def __init__(self, notification_service):
        self.notification_service = notification_service

    def update(self, event: DomainEvent) -> None:
        self.notification_service.handle_event(event)