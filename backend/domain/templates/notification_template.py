from abc import ABC, abstractmethod

from backend.domain.enums.event_type import EventType


class NotificationTemplate(ABC):
    """
    Template Method para construir mensajes de notificación según el canal.
    El flujo general de construcción vive aquí.
    """

    def build_message(self, event_type: EventType, title: str, detail: str) -> str:
        return "\n".join(
            [
                self.header(),
                self.intro(event_type),
                self.body(title, detail),
                self.footer(),
            ]
        )

    def header(self) -> str:
        return "OpsCenter Notification"

    @abstractmethod
    def intro(self, event_type: EventType) -> str:
        ...

    @abstractmethod
    def body(self, title: str, detail: str) -> str:
        ...

    def footer(self) -> str:
        return "Este mensaje fue generado automáticamente por OpsCenter."