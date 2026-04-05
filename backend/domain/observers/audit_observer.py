from backend.domain.observers.observer import Observer
from backend.domain.events.base_event import DomainEvent


class AuditObserver(Observer):
    """
    Observer simple de auditoría.
    Por ahora solo registra en consola cada evento publicado.
    """

    def update(self, event: DomainEvent) -> None:
        print(
            f"[AUDIT] event_type={event.event_type.value} "
            f"event_id={event.event_id} "
            f"occurred_at={event.occurred_at}"
        )