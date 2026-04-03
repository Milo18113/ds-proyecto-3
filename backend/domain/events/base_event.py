from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4
from backend.domain.enums.event_type import EventType


@dataclass
class DomainEvent:
    """
    Clase base para todos los eventos del sistema.
    Cada evento captura qué ocurrió, cuándo, y los datos relevantes.
    No contiene lógica — es solo un contenedor de información.
    """
    event_type: EventType
    occurred_at: datetime = field(default_factory=datetime.utcnow)
    event_id: str = field(default_factory=lambda: str(uuid4()))

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__} "
            f"event_id={self.event_id} occurred_at={self.occurred_at}>"
        )
