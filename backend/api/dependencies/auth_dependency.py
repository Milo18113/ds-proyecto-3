from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.infrastructure.database.connection import get_db
from backend.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from backend.api.guards.role_guard import get_current_user_payload
from backend.domain.entities.user import User


def get_current_user(
    payload: dict = Depends(get_current_user_payload),
    db: Session = Depends(get_db),
) -> User:
    """
    Obtiene el usuario autenticado actual a partir del payload del JWT.
    """
    user_repo = UserRepositoryImpl(db)
    user = user_repo.find_by_id(payload["sub"])

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario autenticado no encontrado.",
        )

    return user