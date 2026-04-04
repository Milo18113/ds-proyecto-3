from backend.domain.repositories.incident_repository import IncidentRepository
from backend.domain.repositories.user_repository import UserRepository
from backend.domain.enums.event_type import EventType
from backend.infrastructure.events.event_bus import EventBus
from backend.application.dtos.incident_dto import AssignIncidentDTO, IncidentResponseDTO


class AssignIncidentUseCase:
    """
    Caso de uso: asignar un incidente a un usuario.
    Solo SUPERVISOR y ADMIN pueden ejecutar este caso de uso.
    Usa el patrón State para validar la transición.
    """

    def __init__(
        self,
        incident_repo: IncidentRepository,
        user_repo: UserRepository,
        event_bus: EventBus,
    ):
        self.incident_repo = incident_repo
        self.user_repo = user_repo
        self.event_bus = event_bus

    def execute(
        self,
        incident_id: str,
        dto: AssignIncidentDTO,
    ) -> IncidentResponseDTO:
        # Validar que el incidente existe
        incident = self.incident_repo.find_by_id(incident_id)
        if not incident:
            raise ValueError(f"Incidente {incident_id} no encontrado.")

        # Validar que el usuario asignado existe
        assignee = self.user_repo.find_by_id(dto.assigned_to)
        if not assignee:
            raise ValueError(f"Usuario {dto.assigned_to} no encontrado.")

        # Transicionar estado (delegado al patrón State)
        incident.assign(dto.assigned_to)

        # Persistir
        updated = self.incident_repo.update(incident)

        # Publicar evento
        self.event_bus.publish(
            EventType.INCIDENT_ASSIGNED,
            {
                "recipient": dto.assigned_to,
                "title": updated.title,
                "detail": f"Asignado a: {assignee.name}",
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
