from backend.domain.repositories.incident_repository import IncidentRepository
from backend.domain.repositories.task_repository import TaskRepository
from backend.application.dtos.incident_dto import IncidentDetailDTO
from backend.application.dtos.task_dto import TaskResponseDTO


class GetIncidentDetailUseCase:
    """
    Caso de uso: ver detalle de un incidente con sus tareas asociadas.
    """

    def __init__(
        self,
        incident_repo: IncidentRepository,
        task_repo: TaskRepository,
    ):
        self.incident_repo = incident_repo
        self.task_repo = task_repo

    def execute(self, incident_id: str) -> IncidentDetailDTO:
        incident = self.incident_repo.find_by_id(incident_id)
        if not incident:
            raise ValueError(f"Incidente {incident_id} no encontrado.")

        tasks = self.task_repo.find_by_incident(incident_id)
        task_dtos = [
            TaskResponseDTO(
                id=t.id,
                incident_id=t.incident_id,
                title=t.title,
                description=t.description,
                status=t.status,
                assigned_to=t.assigned_to,
                created_at=t.created_at,
            )
            for t in tasks
        ]

        return IncidentDetailDTO(
            id=incident.id,
            title=incident.title,
            description=incident.description,
            severity=incident.severity,
            status=incident.status,
            created_by=incident.created_by,
            assigned_to=incident.assigned_to,
            created_at=incident.created_at,
            tasks=task_dtos,
        )
