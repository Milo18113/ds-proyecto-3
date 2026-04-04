from abc import ABC, abstractmethod
from backend.domain.events.base_event import DomainEvent
from backend.domain.observers.observer import Observer


class BaseEventBus(ABC):
    """
    Interfaz abstracta del Event Bus (puerto de salida).
    Define el contrato que debe cumplir cualquier implementación
    concreta del bus, que vivirá en infrastructure/events/.

    De esta forma el dominio y la capa de aplicación dependen
    solo de esta abstracción, nunca de la implementación concreta.
    """

    @abstractmethod
    def subscribe(self, observer: Observer) -> None:
        """Registra un observer para recibir todos los eventos publicados."""
        ...

    @abstractmethod
    def unsubscribe(self, observer: Observer) -> None:
        """Elimina un observer previamente registrado."""
        ...

    @abstractmethod
    def publish(self, event: DomainEvent) -> None:
        """
        Publica un evento y lo entrega a todos los observers suscritos.
        Los casos de uso llaman a este método tras ejecutar su lógica.
        """
        ...
