from backend.domain.events.base_event import DomainEvent
from backend.domain.observers.observer import Observer


class AuditObserver(Observer):
    """
    Observer simple de auditoría.
    Por ahora solo registra en consola cada evento publicado.
    Segundo observer concreto requerido.
    """

    def update(self, event: DomainEvent) -> None:
        print(
            f"[AUDIT] event_id={event.event_id} "
            f"type={event.event_type.value} "
            f"occurred_at={event.occurred_at}"
        )