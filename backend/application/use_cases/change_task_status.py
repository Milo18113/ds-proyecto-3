from backend.domain.repositories.task_repository import TaskRepository
from backend.domain.enums.task_status import TaskStatus
from backend.domain.enums.event_type import EventType
from backend.infrastructure.events.event_bus import EventBus
from backend.application.dtos.task_dto import ChangeTaskStatusDTO, TaskResponseDTO


class ChangeTaskStatusUseCase:
    """
    Caso de uso: cambiar el estado de una tarea.
    Si la tarea pasa a DONE, publica el evento TASK_DONE.
    """

    def __init__(
        self,
        task_repo: TaskRepository,
        event_bus: EventBus,
    ):
        self.task_repo = task_repo
        self.event_bus = event_bus

    def execute(
        self,
        task_id: str,
        dto: ChangeTaskStatusDTO,
    ) -> TaskResponseDTO:
        task = self.task_repo.find_by_id(task_id)
        if not task:
            raise ValueError(f"Tarea {task_id} no encontrada.")

        old_status = task.status
        task.status = dto.status

        updated = self.task_repo.update(task)

        # Publicar evento si la tarea se completó
        if dto.status == TaskStatus.DONE and old_status != TaskStatus.DONE:
            self.event_bus.publish(
                EventType.TASK_DONE,
                {
                    "recipient": updated.assigned_to,
                    "title": updated.title,
                    "detail": f"Incidente asociado: {updated.incident_id}",
                },
            )

        return TaskResponseDTO(
            id=updated.id,
            incident_id=updated.incident_id,
            title=updated.title,
            description=updated.description,
            status=updated.status,
            assigned_to=updated.assigned_to,
            created_at=updated.created_at,
        )
