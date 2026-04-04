from dataclasses import dataclass, field
from backend.domain.events.base_event import DomainEvent
from backend.domain.entities.task import Task
from backend.domain.enums.event_type import EventType


@dataclass
class TaskCreatedEvent(DomainEvent):
    """
    Se publica cuando se crea una tarea asociada a un incidente.
    El observer notificará al usuario asignado (task.assigned_to).
    """
    task: Task = field(default=None)
    event_type: EventType = field(default=EventType.TASK_CREATED, init=False)


@dataclass
class TaskDoneEvent(DomainEvent):
    """
    Se publica cuando una tarea cambia su estado a DONE.
    Puede usarse para notificar al Supervisor del incidente padre.
    """
    task: Task = field(default=None)
    completed_by_id: str = field(default="")    # ID del usuario que marcó como DONE
    event_type: EventType = field(default=EventType.TASK_DONE, init=False)
