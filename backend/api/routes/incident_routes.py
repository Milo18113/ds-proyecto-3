from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.infrastructure.database.connection import get_db
from backend.infrastructure.repositories.incident_repository_impl import IncidentRepositoryImpl
from backend.infrastructure.repositories.task_repository_impl import TaskRepositoryImpl
from backend.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from backend.infrastructure.repositories.notification_repository_impl import NotificationRepositoryImpl
from backend.infrastructure.events.event_bus import EventBus
from backend.domain.observers.notification_observer import NotificationObserver
from backend.domain.observers.audit_observer import AuditObserver
from backend.domain.states.incident_state import InvalidTransitionError

from backend.application.use_cases.create_incident import CreateIncidentUseCase
from backend.application.use_cases.get_incidents import GetIncidentsUseCase
from backend.application.use_cases.get_incident_detail import GetIncidentDetailUseCase
from backend.application.use_cases.assign_incident import AssignIncidentUseCase
from backend.application.use_cases.change_incident_status import ChangeIncidentStatusUseCase

from backend.application.dtos.incident_dto import (
    CreateIncidentDTO,
    AssignIncidentDTO,
    ChangeIncidentStatusDTO,
    IncidentResponseDTO,
    IncidentDetailDTO,
)

from backend.api.dependencies.auth_dependency import get_current_user
from backend.api.guards.role_guard import require_roles
from backend.domain.entities.user import User
from backend.domain.enums.role import Role
from backend.application.services.notification_service import NotificationService

router = APIRouter(prefix="/incidents", tags=["Incidents"])


def _build_event_bus(db: Session) -> EventBus:
    notification_repo = NotificationRepositoryImpl(db)
    notification_service = NotificationService(notification_repo)

    bus = EventBus()
    bus.subscribe(NotificationObserver(notification_service))
    bus.subscribe(AuditObserver())
    return bus


# ── GET /incidents ────────────────────────────────────────────────────────

@router.get("", response_model=list[IncidentResponseDTO])
def list_incidents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Lista incidentes según el rol del usuario autenticado."""
    incident_repo = IncidentRepositoryImpl(db)
    use_case = GetIncidentsUseCase(incident_repo)
    return use_case.execute(current_user)


# ── POST /incidents ───────────────────────────────────────────────────────

@router.post("", response_model=IncidentResponseDTO, status_code=status.HTTP_201_CREATED)
def create_incident(
    dto: CreateIncidentDTO,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Crea un nuevo incidente."""
    incident_repo = IncidentRepositoryImpl(db)
    event_bus = _build_event_bus(db)
    use_case = CreateIncidentUseCase(incident_repo, event_bus)

    try:
        return use_case.execute(dto, created_by=current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# ── GET /incidents/{id} ──────────────────────────────────────────────────

@router.get("/{incident_id}", response_model=IncidentDetailDTO)
def get_incident_detail(
    incident_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Retorna el detalle de un incidente con sus tareas asociadas."""
    incident_repo = IncidentRepositoryImpl(db)
    task_repo = TaskRepositoryImpl(db)
    use_case = GetIncidentDetailUseCase(incident_repo, task_repo)

    try:
        return use_case.execute(incident_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# ── PATCH /incidents/{id}/assign ─────────────────────────────────────────

@router.patch("/{incident_id}/assign", response_model=IncidentResponseDTO)
def assign_incident(
    incident_id: str,
    dto: AssignIncidentDTO,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Asigna un incidente a un usuario. Solo SUPERVISOR y ADMIN."""
    # Guard de rol manual (para inyectar current_user)
    if not current_user.can_assign_incident():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para asignar incidentes.",
        )

    incident_repo = IncidentRepositoryImpl(db)
    user_repo = UserRepositoryImpl(db)
    event_bus = _build_event_bus(db)
    use_case = AssignIncidentUseCase(incident_repo, user_repo, event_bus)

    try:
        return use_case.execute(incident_id, dto)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except InvalidTransitionError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


# ── PATCH /incidents/{id}/status ─────────────────────────────────────────

@router.patch("/{incident_id}/status", response_model=IncidentResponseDTO)
def change_incident_status(
    incident_id: str,
    dto: ChangeIncidentStatusDTO,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Cambia el estado de un incidente. Solo SUPERVISOR y ADMIN."""
    if not current_user.can_change_incident_status():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para cambiar el estado de incidentes.",
        )

    incident_repo = IncidentRepositoryImpl(db)
    event_bus = _build_event_bus(db)
    use_case = ChangeIncidentStatusUseCase(incident_repo, event_bus)

    try:
        return use_case.execute(incident_id, dto, changed_by=current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except InvalidTransitionError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
