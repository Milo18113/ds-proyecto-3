from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.infrastructure.database.connection import get_db
from backend.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from backend.application.dtos.user_dto import UserResponseDTO
from backend.api.guards.role_guard import require_any_role

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", response_model=list[UserResponseDTO])
def list_users(
    _payload: dict = Depends(require_any_role),
    db: Session = Depends(get_db),
):
    """Lista todos los usuarios del sistema (para dropdowns de asignación)."""
    user_repo = UserRepositoryImpl(db)
    users = user_repo.find_all()
    return [
        UserResponseDTO(
            id=u.id,
            name=u.name,
            email=u.email,
            role=u.role,
            created_at=u.created_at,
        )
        for u in users
    ]
