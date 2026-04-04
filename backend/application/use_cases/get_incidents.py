from backend.domain.repositories.incident_repository import IncidentRepository
from backend.domain.entities.user import User
from backend.application.dtos.incident_dto import IncidentResponseDTO


class GetIncidentsUseCase:
    """
    Caso de uso: consultar incidentes según el rol del usuario.
    - OPERATOR: solo sus incidentes (creados o asignados).
    - SUPERVISOR / ADMIN: todos los incidentes.
    """

    def __init__(self, incident_repo: IncidentRepository):
        self.incident_repo = incident_repo

    def execute(self, current_user: User) -> list[IncidentResponseDTO]:
        if current_user.can_view_all_incidents():
            incidents = self.incident_repo.find_all()
        else:
            incidents = self.incident_repo.find_by_creator_or_assigned(current_user.id)

        return [
            IncidentResponseDTO(
                id=inc.id,
                title=inc.title,
                description=inc.description,
                severity=inc.severity,
                status=inc.status,
                created_by=inc.created_by,
                assigned_to=inc.assigned_to,
                created_at=inc.created_at,
            )
            for inc in incidents
        ]
