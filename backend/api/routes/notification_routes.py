from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.infrastructure.database.connection import get_db
from backend.infrastructure.repositories.notification_repository_impl import NotificationRepositoryImpl

from backend.application.use_cases.get_notifications import GetNotificationsUseCase
from backend.application.dtos.notification_dto import NotificationResponseDTO

from backend.api.dependencies.auth_dependency import get_current_user
from backend.domain.entities.user import User

router = APIRouter(prefix="/notifications", tags=["Notifications"])


# ── GET /notifications ────────────────────────────────────────────────────

@router.get("", response_model=list[NotificationResponseDTO])
def list_notifications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Lista notificaciones según el rol del usuario autenticado."""
    notification_repo = NotificationRepositoryImpl(db)
    use_case = GetNotificationsUseCase(notification_repo)
    return use_case.execute(current_user)
