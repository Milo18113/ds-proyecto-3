from backend.domain.events.base_event_bus import BaseEventBus
from backend.domain.observers.observer import Observer
from backend.domain.events.base_event import DomainEvent


class EventBus(BaseEventBus):
    """
    Implementación concreta del Event Bus.
    Mantiene una lista de observers suscritos y les entrega
    cada evento publicado en orden de suscripción.

    Es un Singleton para garantizar que toda la aplicación
    comparte el mismo bus — ese es el patrón creacional adicional
    que justifica la Persona 4 en el README.
    """

    _instance: "EventBus | None" = None
    _observers: list[Observer] = []

    def __new__(cls) -> "EventBus":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._observers = []
        return cls._instance

    def subscribe(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)
            print(f"[EventBus] Observer suscrito: {observer}")

    def unsubscribe(self, observer: Observer) -> None:
        if observer in self._observers:
            self._observers.remove(observer)
            print(f"[EventBus] Observer eliminado: {observer}")

    def publish(self, event: DomainEvent) -> None:
        print(f"[EventBus] Publicando evento: {event.event_type.value}")
        for observer in self._observers:
            try:
                observer.update(event)
            except Exception as e:
                # Un observer fallido no debe detener al resto
                print(f"[EventBus] Error en {observer}: {e}")
