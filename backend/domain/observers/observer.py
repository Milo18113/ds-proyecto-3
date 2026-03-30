from abc import ABC, abstractmethod
from backend.domain.events.base_event import DomainEvent


class Observer(ABC):
    """
    Interfaz abstracta del patrón Observer.
    Todo observer concreto debe implementar update(),
    que recibe el evento publicado y reacciona en consecuencia.

    Las implementaciones concretas viven en infrastructure/
    (Persona 3): NotificationObserver, AuditObserver.
    """

    @abstractmethod
    def update(self, event: DomainEvent) -> None:
        """
        Recibe y procesa un evento del sistema.
        El observer decide internamente si le interesa el evento
        o si lo ignora según su event_type.
        """
        ...

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"
