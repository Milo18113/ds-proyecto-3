from backend.domain.repositories.incident_repository import IncidentRepository
from backend.domain.enums.incident_status import IncidentStatus
from backend.domain.enums.event_type import EventType
from backend.infrastructure.events.event_bus import EventBus
from backend.application.dtos.incident_dto import ChangeIncidentStatusDTO, IncidentResponseDTO


class ChangeIncidentStatusUseCase:
    """
    Caso de uso: cambiar el estado de un incidente.
    Solo SUPERVISOR y ADMIN pueden ejecutar este caso de uso.
    Usa el patrón State para validar las transiciones permitidas.
    """

    def __init__(
        self,
        incident_repo: IncidentRepository,
        event_bus: EventBus,
    ):
        self.incident_repo = incident_repo
        self.event_bus = event_bus

    def execute(
        self,
        incident_id: str,
        dto: ChangeIncidentStatusDTO,
        changed_by: str,
    ) -> IncidentResponseDTO:
        incident = self.incident_repo.find_by_id(incident_id)
        if not incident:
            raise ValueError(f"Incidente {incident_id} no encontrado.")

        # Aplicar transición según el estado solicitado (patrón State)
        transition_map = {
            IncidentStatus.ASSIGNED: incident.assign,
            IncidentStatus.IN_PROGRESS: incident.start_progress,
            IncidentStatus.RESOLVED: incident.resolve,
            IncidentStatus.CLOSED: incident.close,
        }

        action = transition_map.get(dto.status)
        if action is None:
            raise ValueError(f"Estado destino inválido: {dto.status.value}")

        if dto.status == IncidentStatus.ASSIGNED:
            # assign requiere un user_id; si ya tiene asignado, se reasigna
            if not incident.assigned_to:
                raise ValueError(
                    "No se puede cambiar a ASSIGNED sin asignar un usuario. "
                    "Use el endpoint de asignación."
                )
            action(incident.assigned_to)
        else:
            action()

        # Persistir
        updated = self.incident_repo.update(incident)

        # Publicar evento
        recipient = updated.assigned_to or updated.created_by
        self.event_bus.publish(
            EventType.INCIDENT_STATUS_CHANGED,
            {
                "recipient": recipient,
                "title": updated.title,
                "detail": f"Nuevo estado: {updated.status.value}",
            },
        )

        return IncidentResponseDTO(
            id=updated.id,
            title=updated.title,
            description=updated.description,
            severity=updated.severity,
            status=updated.status,
            created_by=updated.created_by,
            assigned_to=updated.assigned_to,
            created_at=updated.created_at,
        )
