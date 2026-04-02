from backend.domain.repositories.task_repository import TaskRepository
from backend.domain.repositories.incident_repository import IncidentRepository
from backend.domain.repositories.user_repository import UserRepository
from backend.domain.factories.entity_factory import TaskFactory
from backend.domain.enums.event_type import EventType
from backend.infrastructure.events.event_bus import EventBus
from backend.application.dtos.task_dto import CreateTaskDTO, TaskResponseDTO


class CreateTaskUseCase:
    """
    Caso de uso: crear una tarea asociada a un incidente existente.
    Persiste la tarea y publica el evento TASK_CREATED.
    """

    def __init__(
        self,
        task_repo: TaskRepository,
        incident_repo: IncidentRepository,
        user_repo: UserRepository,
        event_bus: EventBus,
    ):
        self.task_repo = task_repo
        self.incident_repo = incident_repo
        self.user_repo = user_repo
        self.event_bus = event_bus

    def execute(self, dto: CreateTaskDTO) -> TaskResponseDTO:
        # Validar que el incidente existe
        incident = self.incident_repo.find_by_id(dto.incident_id)
        if not incident:
            raise ValueError(f"Incidente {dto.incident_id} no encontrado.")

        # Validar que el usuario asignado existe
        assignee = self.user_repo.find_by_id(dto.assigned_to)
        if not assignee:
            raise ValueError(f"Usuario {dto.assigned_to} no encontrado.")

        # Crear con Factory
        task = TaskFactory.create(
            incident_id=dto.incident_id,
            title=dto.title,
            description=dto.description,
            assigned_to=dto.assigned_to,
        )

        # Persistir
        saved = self.task_repo.save(task)

        # Publicar evento
        self.event_bus.publish(
            EventType.TASK_CREATED,
            {
                "recipient": dto.assigned_to,
                "title": saved.title,
                "detail": f"Asociada al incidente '{incident.title}'",
            },
        )

        return TaskResponseDTO(
            id=saved.id,
            incident_id=saved.incident_id,
            title=saved.title,
            description=saved.description,
            status=saved.status,
            assigned_to=saved.assigned_to,
            created_at=saved.created_at,
        )
