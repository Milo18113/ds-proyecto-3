from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4
from backend.domain.enums.task_status import TaskStatus


@dataclass
class Task:
    """
    Entidad de dominio que representa una tarea asociada a un incidente.
    Siempre pertenece a un Incident existente (incident_id obligatorio).
    """
    id: str
    incident_id: str                     # FK lógica al incidente padre
    title: str
    description: str
    assigned_to: str                     # ID del usuario responsable
    created_at: datetime = field(default_factory=datetime.utcnow)
    status: TaskStatus = field(default=TaskStatus.OPEN)

    def __post_init__(self):
        if not self.id:
            self.id = str(uuid4())
        self._validate()

    def _validate(self):
        if not self.title or not self.title.strip():
            raise ValueError("El título de la tarea no puede estar vacío.")
        if not self.description or not self.description.strip():
            raise ValueError("La descripción de la tarea no puede estar vacía.")
        if not self.incident_id or not self.incident_id.strip():
            raise ValueError("La tarea debe estar asociada a un incidente.")
        if not self.assigned_to or not self.assigned_to.strip():
            raise ValueError("La tarea debe tener un responsable asignado.")

    def is_done(self) -> bool:
        return self.status == TaskStatus.DONE

    def is_in_progress(self) -> bool:
        return self.status == TaskStatus.IN_PROGRESS

    def __repr__(self) -> str:
        return (
            f"<Task id={self.id} title='{self.title}' "
            f"status={self.status} incident_id={self.incident_id}>"
        )
