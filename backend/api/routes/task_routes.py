from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.infrastructure.database.connection import get_db
from backend.infrastructure.repositories.task_repository_impl import TaskRepositoryImpl
from backend.infrastructure.repositories.incident_repository_impl import IncidentRepositoryImpl
from backend.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from backend.infrastructure.repositories.notification_repository_impl import NotificationRepositoryImpl
from backend.infrastructure.events.event_bus import EventBus
from backend.domain.observers.notification_observer import NotificationObserver
from backend.domain.observers.audit_observer import AuditObserver

from backend.application.use_cases.create_task import CreateTaskUseCase
from backend.application.use_cases.get_tasks import GetTasksUseCase
from backend.application.use_cases.change_task_status import ChangeTaskStatusUseCase

from backend.application.dtos.task_dto import (
    CreateTaskDTO,
    ChangeTaskStatusDTO,
    TaskResponseDTO,
)

from backend.api.dependencies.auth_dependency import get_current_user
from backend.domain.entities.user import User

router = APIRouter(prefix="/tasks", tags=["Tasks"])


def _build_event_bus(db: Session) -> EventBus:
    """Construye el Event Bus con sus observers registrados."""
    notification_repo = NotificationRepositoryImpl(db)
    bus = EventBus()
    bus.subscribe(NotificationObserver(notification_repo))
    bus.subscribe(AuditObserver())
    return bus


# ── GET /tasks ────────────────────────────────────────────────────────────

@router.get("", response_model=list[TaskResponseDTO])
def list_tasks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Lista tareas según el rol del usuario autenticado."""
    task_repo = TaskRepositoryImpl(db)
    use_case = GetTasksUseCase(task_repo)
    return use_case.execute(current_user)


# ── POST /tasks ───────────────────────────────────────────────────────────

@router.post("", response_model=TaskResponseDTO, status_code=status.HTTP_201_CREATED)
def create_task(
    dto: CreateTaskDTO,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Crea una nueva tarea asociada a un incidente existente."""
    task_repo = TaskRepositoryImpl(db)
    incident_repo = IncidentRepositoryImpl(db)
    user_repo = UserRepositoryImpl(db)
    event_bus = _build_event_bus(db)
    use_case = CreateTaskUseCase(task_repo, incident_repo, user_repo, event_bus)

    try:
        return use_case.execute(dto)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# ── PATCH /tasks/{id}/status ─────────────────────────────────────────────

@router.patch("/{task_id}/status", response_model=TaskResponseDTO)
def change_task_status(
    task_id: str,
    dto: ChangeTaskStatusDTO,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Cambia el estado de una tarea."""
    task_repo = TaskRepositoryImpl(db)
    event_bus = _build_event_bus(db)
    use_case = ChangeTaskStatusUseCase(task_repo, event_bus)

    try:
        return use_case.execute(task_id, dto)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
