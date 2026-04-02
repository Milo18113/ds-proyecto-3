from backend.domain.repositories.task_repository import TaskRepository
from backend.domain.entities.user import User
from backend.application.dtos.task_dto import TaskResponseDTO


class GetTasksUseCase:
    """
    Caso de uso: consultar tareas según el rol del usuario.
    - OPERATOR: solo sus tareas asignadas.
    - SUPERVISOR / ADMIN: todas las tareas.
    """

    def __init__(self, task_repo: TaskRepository):
        self.task_repo = task_repo

    def execute(self, current_user: User) -> list[TaskResponseDTO]:
        if current_user.can_view_all_tasks():
            tasks = self.task_repo.find_all()
        else:
            tasks = self.task_repo.find_by_assigned(current_user.id)

        return [
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
