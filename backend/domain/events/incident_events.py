from dataclasses import dataclass, field
from backend.domain.events.base_event import DomainEvent
from backend.domain.entities.incident import Incident
from backend.domain.enums.event_type import EventType
from backend.domain.enums.incident_status import IncidentStatus


@dataclass
class IncidentCreatedEvent(DomainEvent):
    """
    Se publica cuando un usuario crea un incidente nuevo.
    Los observers usarán incident.assigned_to y incident.created_by
    para saber a quién notificar.
    """
    incident: Incident = field(default=None)
    event_type: EventType = field(default=EventType.INCIDENT_CREATED, init=False)


@dataclass
class IncidentAssignedEvent(DomainEvent):
    """
    Se publica cuando un Supervisor o Admin asigna un incidente
    a un usuario. El campo assigned_to_id indica el destinatario.
    """
    incident: Incident = field(default=None)
    assigned_to_id: str = field(default="")     # ID del usuario recién asignado
    assigned_by_id: str = field(default="")     # ID del Supervisor/Admin que asignó
    event_type: EventType = field(default=EventType.INCIDENT_ASSIGNED, init=False)


@dataclass
class IncidentStatusChangedEvent(DomainEvent):
    """
    Se publica cuando el estado de un incidente cambia.
    Incluye el estado anterior y el nuevo para que los observers
    puedan construir mensajes contextuales.
    """
    incident: Incident = field(default=None)
    previous_status: IncidentStatus = field(default=None)
    new_status: IncidentStatus = field(default=None)
    changed_by_id: str = field(default="")      # ID del usuario que hizo el cambio
    event_type: EventType = field(default=EventType.INCIDENT_STATUS_CHANGED, init=False)
