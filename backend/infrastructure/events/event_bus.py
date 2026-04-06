from backend.domain.events.base_event_bus import BaseEventBus
from backend.domain.observers.observer import Observer
from backend.domain.events.base_event import DomainEvent


class EventBus(BaseEventBus):
    """
    Implementación concreta del Event Bus.
    Mantiene una lista de observers suscritos y les entrega
    cada evento publicado en orden de suscripción.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._observers = []
        return cls._instance

    def subscribe(self, observer: Observer) -> None:
        already_registered = any(type(o) is type(observer) for o in self._observers)
        if not already_registered:
            self._observers.append(observer)

    def unsubscribe(self, observer: Observer) -> None:
        self._observers = [o for o in self._observers if type(o) is not type(observer)]

    def publish(self, event: DomainEvent) -> None:
        for observer in self._observers:
            try:
                observer.update(event)
            except Exception as e:
                print(f"[EventBus] Error en {observer}: {e}")