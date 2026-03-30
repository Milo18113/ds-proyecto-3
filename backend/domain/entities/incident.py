from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4
from backend.domain.enums.severity import Severity
from backend.domain.enums.incident_status import IncidentStatus
from backend.domain.states.incident_state import IncidentState


@dataclass
class Incident:
    """
    Entidad de dominio que representa un incidente operativo.
    El ciclo de vida (estado) se controla mediante el patrón State,
    implementado en backend/domain/states/.
    """
    id: str
    title: str
    description: str
    severity: Severity
    created_by: str                      # ID del usuario que creó el incidente
    created_at: datetime = field(default_factory=datetime.utcnow)
    status: IncidentStatus = field(default=IncidentStatus.OPEN)
    assigned_to: str | None = None       # ID del usuario asignado (opcional)
    state: IncidentState = field(init=False)       # Estado actual (patrón State)

    def __post_init__(self):
        if not self.id:
            self.id = str(uuid4())
        from backend.domain.states.open_state import OpenState
        self.state = OpenState()  # Initial state
        self._validate()

    def _validate(self):
        if not self.title or not self.title.strip():
            raise ValueError("El título del incidente no puede estar vacío.")
        if not self.description or not self.description.strip():
            raise ValueError("La descripción del incidente no puede estar vacía.")
        if not isinstance(self.severity, Severity):
            raise ValueError(f"Severidad inválida: {self.severity}")


    # ── Transiciones de estado (delegadas al patrón State) ────────────────
 
    def assign(self, user_id: str) -> None:
        """Asigna el incidente a un usuario y transiciona a ASSIGNED."""
        self.state.assign(self)
        self.assigned_to = user_id
 
    def start_progress(self) -> None:
        """Transiciona el incidente a IN_PROGRESS."""
        self.state.start_progress(self)
 
    def resolve(self) -> None:
        """Transiciona el incidente a RESOLVED."""
        self.state.resolve(self)
 
    def close(self) -> None:
        """Transiciona el incidente a CLOSED."""
        self.state.close(self)
 

    # ── Helpers ───────────────────────────────────────────────────────────
 
    def is_open(self) -> bool:
        return self.status == IncidentStatus.OPEN
 
    def is_closed(self) -> bool:
        return self.status == IncidentStatus.CLOSED
 
    def is_assigned(self) -> bool:
        return self.assigned_to is not None
 
    def __repr__(self) -> str:
        return (
            f"<Incident id={self.id} title='{self.title}' "
            f"status={self.status} severity={self.severity}>"
        )
